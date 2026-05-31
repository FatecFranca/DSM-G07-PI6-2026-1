package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Batimento;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.Date;

@Repository
public interface BatimentoRepository extends MongoRepository<Batimento, String> {

    Page<Batimento> findAllByAnimal(String animal, Pageable pageable);
    Page<Batimento> findAllByAnimalAndDataBetween(String animal, Date dataInicio, Date dataFim, Pageable pageable);
    Page<Batimento> findAllByColeira(String coleira, Pageable pageable);
    Page<Batimento> findAllByColeiraAndDataBetween(String coleira, Date dataInicio, Date dataFim, Pageable pageable);

    /**
     * Busca o último batimento cardíaco registrado de um animal (ordenado por data decrescente)
     * @param animal ID do animal
     * @return Optional contendo o último batimento se existir
     */
    Optional<Batimento> findFirstByAnimalOrderByDataDesc(String animal);
}
