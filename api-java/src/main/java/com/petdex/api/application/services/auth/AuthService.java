package com.petdex.api.application.services.auth;

import com.petdex.api.application.contracts.dto.auth.LoginReqDTO;
import com.petdex.api.application.contracts.dto.auth.LoginResDTO;

public interface AuthService {
    LoginResDTO login(LoginReqDTO loginReqDTO);
}
