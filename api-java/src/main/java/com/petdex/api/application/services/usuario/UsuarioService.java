package com.petdex.api.application.services.usuario;

import com.petdex.api.application.contracts.dto.PageDTO;
import com.petdex.api.application.contracts.dto.usuario.UsuarioReqDTO;
import com.petdex.api.application.contracts.dto.usuario.UsuarioResDTO;
import org.springframework.data.domain.Page;

public interface UsuarioService {

    UsuarioResDTO findById(String id);
    Page<UsuarioResDTO> findAll(PageDTO pageDTO);
    UsuarioResDTO create (UsuarioReqDTO usuarioDTO);
    UsuarioResDTO update (String id, UsuarioReqDTO usuarioReqDTO);
    void delete (String id);

}
