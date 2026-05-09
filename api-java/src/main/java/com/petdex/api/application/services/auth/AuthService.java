package com.petdex.api.application.services.auth;

import com.petdex.api.domain.contracts.dto.auth.LoginReqDTO;
import com.petdex.api.domain.contracts.dto.auth.LoginResDTO;

public interface AuthService {
    LoginResDTO login(LoginReqDTO loginReqDTO);
}
