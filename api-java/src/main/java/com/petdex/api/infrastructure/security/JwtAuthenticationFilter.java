package com.petdex.api.infrastructure.security;

import com.petdex.api.application.services.security.TokenService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.ArrayList;


@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    @Autowired
    private TokenService tokenService;


    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {


        final String authHeader = request.getHeader("Authorization");
        final String jwt;
        final String userId;

         if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            logger.info("Requisição sem token JWT: {}", request.getRequestURI());
            filterChain.doFilter(request, response);
            return;
        }

        jwt = authHeader.substring(7);

        try {
            if (tokenService.validateToken(jwt)) {
                userId = tokenService.extractUserId(jwt);

                if (userId != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                            userId,
                            null,
                            new ArrayList<>()
                    );

                    authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                    SecurityContextHolder.getContext().setAuthentication(authToken);
                }
            }
        } catch (io.jsonwebtoken.ExpiredJwtException e) {
            logger.error("Token JWT expirado: {}", e.getMessage());
            request.setAttribute("jwt_error", "Token JWT expirado");
        } catch (io.jsonwebtoken.MalformedJwtException e) {
            logger.error("Token JWT malformado: {}", e.getMessage());
            request.setAttribute("jwt_error", "Token JWT malformado ou inválido");
        } catch (io.jsonwebtoken.security.SignatureException e) {
            logger.error("Assinatura do token JWT inválida: {}", e.getMessage());
            request.setAttribute("jwt_error", "Assinatura do token JWT inválida");
        } catch (Exception e) {
            logger.error("Erro ao validar token JWT: {}", e.getMessage());
            request.setAttribute("jwt_error", "Erro ao validar token JWT: " + e.getMessage());
        }

        filterChain.doFilter(request, response);
    }
}

