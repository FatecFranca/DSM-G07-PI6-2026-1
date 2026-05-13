package com.petdex.api.infrastructure.security;

import com.petdex.api.application.services.security.TokenService;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;


@Service
public class JwtTokenService implements TokenService {

    private static final Logger logger = LoggerFactory.getLogger(JwtTokenService.class);

    @Value("${jwt.secret}")
    private String secretKey;

    private SecretKey getSigningKey() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] keyBytes = digest.digest(secretKey.getBytes(StandardCharsets.UTF_8));
            return Keys.hmacShaKeyFor(keyBytes);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Erro ao gerar chave de assinatura JWT", e);
        }
    }


    public String generateToken(String userId, String email) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("userId", userId);
        claims.put("email", email);
        return createToken(claims, userId);
    }

    private String createToken(Map<String, Object> claims, String subject) {
        Date now = new Date();

        return Jwts.builder()
                .claims(claims)
                .subject(subject)
                .issuedAt(now)
                .signWith(getSigningKey())
                .compact();
    }

    public String extractUserId(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    public String extractEmail(String token) {
        return extractClaim(token, claims -> claims.get("email", String.class));
    }




    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        try {
            Claims claims = Jwts.parser()
                    .verifyWith(getSigningKey())
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
            return claims;
        } catch (Exception e) {
            logger.error("Erro ao extrair claims do token: " + e.getMessage(), e);
            throw e;
        }
    }

    public Boolean validateToken(String token, String userId) {
        try {
            final String extractedUserId = extractUserId(token);
            return extractedUserId.equals(userId);
        } catch (Exception e) {
            return false;
        }
    }

    public Boolean validateToken(String token) {
        try {
            extractAllClaims(token);
            return true;
        } catch (Exception e) {
            logger.error("Token JWT inválido: " + e.getMessage(), e);
            return false;
        }
    }
}

