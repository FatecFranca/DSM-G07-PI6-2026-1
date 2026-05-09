package com.petdex.api.infrastructure.security;

import com.petdex.api.application.services.security.EncryptionService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class BCryptEncryptionService implements EncryptionService {

    private final BCryptPasswordEncoder passwordEncoder;


    public BCryptEncryptionService(@Value("${bcrypt.salt:10}") int strength) {
        this.passwordEncoder = new BCryptPasswordEncoder(strength);
    }

    public String hashPassword(String rawPassword) {
        if (rawPassword == null || rawPassword.isEmpty()) {
            throw new IllegalArgumentException("A senha não pode ser nula ou vazia");
        }
        return passwordEncoder.encode(rawPassword);
    }

    public boolean validatePassword(String rawPassword, String hashedPassword) {
        if (rawPassword == null || hashedPassword == null) {
            return false;
        }
        return passwordEncoder.matches(rawPassword, hashedPassword);
    }
}

