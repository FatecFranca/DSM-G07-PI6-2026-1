package com.petdex.api.application.services.animal;

import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.Especie;
import com.petdex.api.domain.collections.Raca;
import com.petdex.api.domain.contracts.dto.PageDTO;
import com.petdex.api.domain.contracts.dto.animal.AnimalReqDTO;
import com.petdex.api.domain.contracts.dto.animal.AnimalResDTO;
import com.petdex.api.infrastructure.exception.ResourceNotFoundException;
import com.petdex.api.infrastructure.mongodb.AnimalRepository;
import com.petdex.api.infrastructure.mongodb.EspecieRepository;
import com.petdex.api.infrastructure.mongodb.RacaRepository;
import com.petdex.api.infrastructure.mongodb.UsuarioRepository;
import com.petdex.api.application.services.ValidationService;
import org.modelmapper.ModelMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ImplAnimalService implements AnimalService {

    private static final Logger logger = LoggerFactory.getLogger(ImplAnimalService.class);

    @Autowired
    ModelMapper mapper;

    @Autowired
    AnimalRepository animalRepository;

    @Autowired
    EspecieRepository especieRepository;

    @Autowired
    RacaRepository racaRepository;

    @Autowired
    UsuarioRepository usuarioRepository;

    @Autowired
    ValidationService validation;

    @Override
    public AnimalResDTO findById(String id) {
        Animal animal = animalRepository.findById(id).orElseThrow(() -> {
            logger.error("Animal não encontrado com ID: {}", id);
            return new ResourceNotFoundException("Animal", "ID", id);
        });
        Raca raca = racaRepository.findById(animal.getRaca()).orElseThrow(() -> {
            logger.error("Raça {} não encontrada para o animal {}", animal.getRaca(), id);
            return new ResourceNotFoundException("Raça", "ID", animal.getRaca());
        });
        Especie especie = especieRepository.findById(raca.getEspecie()).orElseThrow(()-> {
            logger.error("Espécie {} não encontrada para a raça {}", raca.getEspecie(), raca.getId());
            return new ResourceNotFoundException("Espécie", "ID", raca.getEspecie());
        });

        AnimalResDTO animalResDTO = mapper.map(animal, AnimalResDTO.class);

        animalResDTO.setEspecieNome(especie.getNome());
        animalResDTO.setRacaNome(raca.getNome());


        return animalResDTO;
    }

    @Override
    public Page<AnimalResDTO> findAll(PageDTO pageDTO) {
        pageDTO.sortByName();
        Page<Animal> animaisPage = animalRepository.findAll(pageDTO.mapPage());

        List<AnimalResDTO> dtoList = animaisPage.getContent().stream().map(animal -> {
            AnimalResDTO dto = mapper.map(animal, AnimalResDTO.class);


            Raca raca = racaRepository.findById(animal.getRaca())
                    .orElseThrow(() -> new ResourceNotFoundException("Raça", "ID", animal.getRaca()));


            Especie especie = especieRepository.findById(raca.getEspecie())
                    .orElseThrow(() -> new ResourceNotFoundException("Espécie", "ID", raca.getEspecie()));

            dto.setRacaNome(raca.getNome());
            dto.setEspecieNome(especie.getNome());

            return dto;
        }).toList();

        return new PageImpl<>(dtoList, pageDTO.mapPage(), animaisPage.getTotalElements());
    }

    @Override
    public AnimalResDTO create(AnimalReqDTO animalDTO) throws IOException {
        if (!usuarioRepository.existsById(animalDTO.getUsuario())) {
            logger.error("Falha ao cadastrar animal: Usuário ID {} não encontrado", animalDTO.getUsuario());
            throw new ResourceNotFoundException("Usuário", "ID", animalDTO.getUsuario());
        }

        if (!racaRepository.existsById(animalDTO.getRaca())) {
            logger.error("Falha ao cadastrar animal: Raça ID {} não encontrada", animalDTO.getRaca());
            throw new ResourceNotFoundException("Raça", "ID", animalDTO.getRaca());
        }

        try {
            Animal animal = mapper.map(animalDTO, Animal.class);
            AnimalResDTO res = mapper.map(animalRepository.save(animal), AnimalResDTO.class);
            logger.info("Animal cadastrado com sucesso: {} (ID: {})", res.getNome(), res.getId());
            return res;
        } catch (Exception e) {
            logger.error("Erro ao cadastrar animal: {}", e.getMessage());
            throw e;
        }
    }

    @Override
    public AnimalResDTO update(String id, AnimalReqDTO animalDTO) throws IOException {

        Animal animalUpdate = animalRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Animal", "ID", id));

        if(animalDTO.getNome() != null) animalUpdate.setNome(animalDTO.getNome());
        if(animalDTO.getCastrado() != null) animalUpdate.setCastrado(animalDTO.getCastrado());
        if(animalDTO.getPeso() != null) animalUpdate.setPeso(animalDTO.getPeso());
        if(animalDTO.getRaca() != null) {
            if (!racaRepository.existsById(animalDTO.getRaca())) {
                logger.error("Falha ao atualizar animal: Raça ID {} não encontrada", animalDTO.getRaca());
                throw new ResourceNotFoundException("Raça", "ID", animalDTO.getRaca());
            }
            animalUpdate.setRaca(animalDTO.getRaca());
        }
        if(animalDTO.getDataNascimento() != null) animalUpdate.setDataNascimento(animalDTO.getDataNascimento());
        if(animalDTO.getSexo() != null) animalUpdate.setSexo(animalDTO.getSexo());
        if(animalDTO.getUsuario() != null) {
            if (!usuarioRepository.existsById(animalDTO.getUsuario())) {
                logger.error("Falha ao atualizar animal: Usuário ID {} não encontrado", animalDTO.getUsuario());
                throw new ResourceNotFoundException("Usuário", "ID", animalDTO.getUsuario());
            }
            animalUpdate.setUsuario(animalDTO.getUsuario());
        }

        return mapper.map(animalRepository.save(animalUpdate), AnimalResDTO.class);
    }

    @Override
    public void delete(String id) {
        animalRepository.deleteById(id);
    }

    @Override
    public Optional<AnimalResDTO> findByUsuarioId(String usuarioId) {
        Optional<Animal> animalOpt = animalRepository.findByUsuario(usuarioId);

        return animalOpt.map(animal -> {
            Raca raca = racaRepository.findById(animal.getRaca())
                    .orElseThrow(() -> new ResourceNotFoundException("Raça", "ID", animal.getRaca()));

            Especie especie = especieRepository.findById(raca.getEspecie())
                    .orElseThrow(() -> new ResourceNotFoundException("Espécie", "ID", raca.getEspecie()));

            AnimalResDTO animalResDTO = mapper.map(animal, AnimalResDTO.class);
            animalResDTO.setEspecieNome(especie.getNome());
            animalResDTO.setRacaNome(raca.getNome());

            return animalResDTO;
        });
    }

    @Override
    public String saveImage (String id, MultipartFile file) throws IOException {

        Animal animal = animalRepository.findById(id).orElseThrow(() -> {
            logger.error("Falha ao salvar imagem: Animal não encontrado com ID: {}", id);
            return new ResourceNotFoundException("Animal", "ID", id);
        });

        try {
            String oldImageUrl = animal.getUrlImagem();
            if (oldImageUrl != null && !oldImageUrl.isEmpty()) {
                String oldFileName = oldImageUrl.substring(oldImageUrl.lastIndexOf("/") + 1);
                Path oldFilePath = Paths.get("/uploads/animais/").resolve(oldFileName);

                if (Files.exists(oldFilePath)) {
                    Files.delete(oldFilePath);
                    logger.info("Imagem antiga removida: {}", oldFileName);
                }
            }

            String fileName = UUID.randomUUID() + "_" + file.getOriginalFilename();
            Path uploadPath = Paths.get("/uploads/animais/");
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }
            Path filePath = uploadPath.resolve(fileName);
            Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
            String imageUrl = "/uploads/animais/" + fileName;

            animal.setUrlImagem(imageUrl);
            animalRepository.save(animal);

            logger.info("Nova imagem salva para o animal {}: {}", id, imageUrl);
            return imageUrl;
        } catch (IOException e) {
            logger.error("Erro ao processar upload de imagem para o animal {}: {}", id, e.getMessage());
            throw e;
        }
    }

}
