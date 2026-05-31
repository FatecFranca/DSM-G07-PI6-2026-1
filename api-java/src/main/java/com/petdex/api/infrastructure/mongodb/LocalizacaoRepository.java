package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Localizacao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;
import java.util.Date;

public interface LocalizacaoRepository extends MongoRepository<Localizacao, String> {
    Page<Localizacao> findAllByAnimal(String animal, Pageable pageable);
    Page<Localizacao> findAllByAnimalAndDataBetween(String animal, Date dataInicio, Date dataFim, Pageable pageable);
    Page<Localizacao> findAllByColeira(String coleira, Pageable pageable);
    Page<Localizacao> findAllByColeiraAndDataBetween(String coleira, Date dataInicio, Date dataFim, Pageable pageable);

    /**
     * Busca a última localização registrada de um animal (ordenada por data decrescente)
     * @param animal ID do animal
     * @param pageable Configuração de paginação (deve ter size=1 e ordenação por data desc)
     * @return Optional contendo a última localização se existir
     */
    Optional<Localizacao> findFirstByAnimalOrderByDataDesc(String animal);
}
