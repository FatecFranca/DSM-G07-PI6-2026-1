package com.petdex.api.infrastructure.security;

import com.petdex.api.application.services.security.JwtService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;
import org.springframework.messaging.support.MessageHeaderAccessor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class WebSocketAuthInterceptor implements ChannelInterceptor {
    
    private static final Logger logger = LoggerFactory.getLogger(WebSocketAuthInterceptor.class);

    @Autowired
    private JwtService jwtService;

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);

        if (accessor != null && StompCommand.CONNECT.equals(accessor.getCommand())) {
            String token = extractToken(accessor);

            if (token != null) {
                try {
                    if (jwtService.validateToken(token)) {
                        String userId = jwtService.extractUserId(token);

                        if (userId != null) {
                            UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                                    userId,
                                    null,
                                    new ArrayList<>()
                            );

                            SecurityContextHolder.getContext().setAuthentication(authToken);
                            accessor.setUser(authToken);
                        }
                    }
                } catch (Exception e) {
                    logger.error("Erro ao validar token JWT no WebSocket: {}", e.getMessage());
                }
            }
        }

        return message;
    }

    private String extractToken(StompHeaderAccessor accessor) {
        List<String> authHeaders = accessor.getNativeHeader("Authorization");
        if (authHeaders != null && !authHeaders.isEmpty()) {
            String authHeader = authHeaders.get(0);
            if (authHeader != null && authHeader.startsWith("Bearer ")) {
                return authHeader.substring(7);
            }
        }
        List<String> tokenParams = accessor.getNativeHeader("token");
        if (tokenParams != null && !tokenParams.isEmpty()) {
            return tokenParams.get(0);
        }

        return null;
    }
}

