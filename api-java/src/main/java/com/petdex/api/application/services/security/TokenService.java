package com.petdex.api.application.services.security;

import java.util.Map;
import java.util.function.Function;
import io.jsonwebtoken.Claims;


public interface TokenService {
    String generateToken(String userId, String email);
    String extractUserId(String token);
    String extractEmail(String token);
    <T> T extractClaim(String token, Function<Claims, T> claimsResolver);
    Boolean validateToken(String token, String userId);
    Boolean validateToken(String token);
}
