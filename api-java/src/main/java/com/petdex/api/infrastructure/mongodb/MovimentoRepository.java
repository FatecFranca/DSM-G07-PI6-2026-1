package com.petdex.api.infrastructure.mongodb;

import com.petdex.api.domain.collections.Movimento;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.Date;

public interface MovimentoRepository extends MongoRepository<Movimento, String> {
    Page<Movimento> findAllByAnimal(String animalId, Pageable pageable);
    Page<Movimento> findAllByAnimalAndDataBetween(String animalId, Date dataInicio, Date dataFim, Pageable pageable);
    Page<Movimento> findAllByColeira(String coleiraId, Pageable pageable);
    Page<Movimento> findAllByColeiraAndDataBetween(String coleiraId, Date dataInicio, Date dataFim, Pageable pageable);
}
