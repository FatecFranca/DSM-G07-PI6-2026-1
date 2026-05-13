package com.petdex.api.application.services.movimento;

import com.petdex.api.domain.collections.Movimento;
import com.petdex.api.application.contracts.dto.movimento.MovimentoReqDTO;
import com.petdex.api.application.contracts.dto.movimento.MovimentoResDTO;
import com.petdex.api.infrastructure.mongodb.MovimentoRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.modelmapper.ModelMapper;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Optional;

@ExtendWith(SpringExtension.class)
public class MovimentoServiceTest {

    @InjectMocks
    private MovimentoService service;

    @Mock
    private MovimentoRepository repository;

    @Spy
    private ModelMapper mapper = new ModelMapper();

    @Test
    public void deveSalvarMovimentoComSucesso() {
        // cenário
        MovimentoReqDTO req = new MovimentoReqDTO();
        req.setAnimal("animal123");

        Movimento movimentoSalvo = new Movimento();
        movimentoSalvo.setId("123");

        Mockito.when(repository.save(Mockito.any(Movimento.class))).thenReturn(movimentoSalvo);

        // ação
        MovimentoResDTO result = service.save(req);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Mockito.verify(repository, Mockito.times(1)).save(Mockito.any());
    }

    @Test
    public void deveBuscarMovimentoPorIdComSucesso() {
        // cenário
        String id = "123";
        Movimento movimento = new Movimento();
        movimento.setId(id);

        Mockito.when(repository.findById(id)).thenReturn(Optional.of(movimento));

        // ação
        MovimentoResDTO result = service.fidById(id);

        // verificação
        Assertions.assertThat(result).isNotNull();
        Assertions.assertThat(result.getId()).isEqualTo(id);
    }
}
