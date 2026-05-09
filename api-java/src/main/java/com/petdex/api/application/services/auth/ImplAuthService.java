package com.petdex.api.application.services.auth;

import com.petdex.api.application.services.security.JwtService;
import com.petdex.api.application.services.security.PasswordService;
import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.Usuario;
import com.petdex.api.domain.contracts.dto.auth.LoginReqDTO;
import com.petdex.api.domain.contracts.dto.auth.LoginResDTO;
import com.petdex.api.infrastructure.mongodb.AnimalRepository;
import com.petdex.api.infrastructure.mongodb.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class ImplAuthService implements AuthService {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private AnimalRepository animalRepository;

    @Autowired
    private PasswordService passwordService;

    @Autowired
    private JwtService jwtService;

    @Override
    public LoginResDTO login(LoginReqDTO loginReqDTO) {
        Usuario usuario = usuarioRepository.findByEmail(loginReqDTO.getEmail())
                .orElseThrow(() -> new RuntimeException("Credenciais inválidas"));


        if (!passwordService.validatePassword(loginReqDTO.getSenha(), usuario.getSenha())) {
            throw new RuntimeException("Credenciais inválidas");
        }

        String token = jwtService.generateToken(usuario.getId(), usuario.getEmail());

        Optional<Animal> animalOpt = animalRepository.findByUsuario(usuario.getId());
        String animalId = animalOpt.map(Animal::getId).orElse(null);
        String petName = animalOpt.map(Animal::getNome).orElse(null);
        String animalImagemUrl = animalOpt.map(Animal::getUrlImagem).orElse(null);
        
        return new LoginResDTO(
                token,
                animalId,
                usuario.getId(),
                usuario.getNome(),
                usuario.getEmail(),
                petName,
                animalImagemUrl
        );
    }
}
