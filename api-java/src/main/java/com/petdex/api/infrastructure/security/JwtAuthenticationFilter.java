package com.petdex.api.infrastructure.security;

import com.petdex.api.application.services.security.JwtService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Filtro de autenticação JWT que intercepta todas as requisições
 * Valida o token JWT presente no header Authorization
 */
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Autowired
    private JwtService jwtService;

    /**
     * Intercepta cada requisição HTTP e valida o token JWT
     * @param request Requisição HTTP
     * @param response Resposta HTTP
     * @param filterChain Cadeia de filtros
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {


        // Extrai o header Authorization
        final String authHeader = request.getHeader("Authorization");
        final String jwt;
        final String userId;

        // Log do header Authorization
        // Se não houver header ou não começar com "Bearer ", continua sem autenticação
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        // Extrai o token (remove "Bearer " do início)
        jwt = authHeader.substring(7);

        try {
            // Valida o token e extrai o userId
            if (jwtService.validateToken(jwt)) {
                userId = jwtService.extractUserId(jwt);

                // Se o token é válido e não há autenticação no contexto
                if (userId != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    // Cria um objeto de autenticação
                    UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                            userId,
                            null,
                            new ArrayList<>() // Sem roles/authorities por enquanto
                    );

                    authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                    // Define a autenticação no contexto de segurança
                    SecurityContextHolder.getContext().setAuthentication(authToken);
                }
            }
        } catch (io.jsonwebtoken.ExpiredJwtException e) {
            request.setAttribute("jwt_error", "Token JWT expirado");
        } catch (io.jsonwebtoken.MalformedJwtException e) {
            request.setAttribute("jwt_error", "Token JWT malformado ou inválido");
        } catch (io.jsonwebtoken.security.SignatureException e) {
            request.setAttribute("jwt_error", "Assinatura do token JWT inválida");
        } catch (Exception e) {
            // Token inválido - continua sem autenticação
            request.setAttribute("jwt_error", "Erro ao validar token JWT: " + e.getMessage());
        }

        // Continua a cadeia de filtro
        filterChain.doFilter(request, response);
    }
}

