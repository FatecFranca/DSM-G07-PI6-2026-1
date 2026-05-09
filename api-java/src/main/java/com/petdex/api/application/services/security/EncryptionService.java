package com.petdex.api.application.services.security;

public interface EncryptionService {
    String hashPassword(String rawPassword);
    boolean validatePassword(String rawPassword, String hashedPassword);
}
