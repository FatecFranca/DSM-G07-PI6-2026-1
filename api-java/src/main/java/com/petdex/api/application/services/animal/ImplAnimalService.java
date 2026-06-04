package com.petdex.api.application.services.animal;

import com.petdex.api.domain.collections.Animal;
import com.petdex.api.domain.collections.Especie;
import com.petdex.api.domain.collections.Raca;
import com.petdex.api.application.contracts.dto.PageDTO;
import com.petdex.api.application.contracts.dto.animal.AnimalReqDTO;
import com.petdex.api.application.contracts.dto.animal.AnimalResDTO;
import com.petdex.api.infrastructure.exception.BadRequestException;
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
            Animal savedAnimal = animalRepository.save(animal);

            Raca raca = racaRepository.findById(savedAnimal.getRaca()).orElseThrow(() -> {
                logger.error("Raça {} não encontrada para o animal {}", savedAnimal.getRaca(), savedAnimal.getId());
                return new ResourceNotFoundException("Raça", "ID", savedAnimal.getRaca());
            });
            Especie especie = especieRepository.findById(raca.getEspecie()).orElseThrow(()-> {
                logger.error("Espécie {} não encontrada para a raça {}", raca.getEspecie(), raca.getId());
                return new ResourceNotFoundException("Espécie", "ID", raca.getEspecie());
            });

            AnimalResDTO res = mapper.map(savedAnimal, AnimalResDTO.class);
            res.setRacaNome(raca.getNome());
            res.setEspecieNome(especie.getNome());

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
        if(animalDTO.getCaminhadaDiariaKm() != null) animalUpdate.setCaminhadaDiariaKm(animalDTO.getCaminhadaDiariaKm());
        if(animalDTO.getPorte() != null) animalUpdate.setPorte(animalDTO.getPorte());

        Animal savedAnimal = animalRepository.save(animalUpdate);

        Raca raca = racaRepository.findById(savedAnimal.getRaca()).orElseThrow(() -> {
            logger.error("Raça {} não encontrada para o animal {}", savedAnimal.getRaca(), savedAnimal.getId());
            return new ResourceNotFoundException("Raça", "ID", savedAnimal.getRaca());
        });
        Especie especie = especieRepository.findById(raca.getEspecie()).orElseThrow(()-> {
            logger.error("Espécie {} não encontrada para a raça {}", raca.getEspecie(), raca.getId());
            return new ResourceNotFoundException("Espécie", "ID", raca.getEspecie());
        });

        AnimalResDTO res = mapper.map(savedAnimal, AnimalResDTO.class);
        res.setRacaNome(raca.getNome());
        res.setEspecieNome(especie.getNome());

        return res;
    }

    @Override
    public void delete(String id) {
        animalRepository.deleteById(id);
    }

    @Override
    public Optional<AnimalResDTO> findByUsuarioId(String usuarioId) {
        // Busca o animal pelo ID do usuário
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
        logger.info("Iniciando processo de salvamento de imagem para o animal ID: {}", id);

        Animal animal = animalRepository.findById(id).orElseThrow(() -> {
            logger.error("Falha ao salvar imagem: Animal não encontrado com ID: {}", id);
            return new ResourceNotFoundException("Animal", "ID", id);
        });

        if (file == null || file.isEmpty()) {
            logger.error("Falha ao salvar imagem para o animal ID {}: o arquivo enviado é nulo ou vazio", id);
            throw new BadRequestException("O arquivo de imagem não pode ser nulo ou vazio");
        }

        try {
            // Verifica se existe uma imagem antiga e a exclui
            String oldImageUrl = animal.getUrlImagem();
            if (oldImageUrl != null && !oldImageUrl.isEmpty()) {
                logger.info("Animal ID {} já possui uma imagem: {}. Removendo imagem anterior...", id, oldImageUrl);
                // Extrai o nome do arquivo da URL antiga
                String oldFileName = oldImageUrl.substring(oldImageUrl.lastIndexOf("/") + 1);
                Path oldFilePath = Paths.get("/uploads/animais/").resolve(oldFileName);

                // Exclui o arquivo antigo se ele existir
                if (Files.exists(oldFilePath)) {
                    Files.delete(oldFilePath);
                    logger.info("Imagem antiga removida com sucesso: {}", oldFileName);
                } else {
                    logger.warn("Imagem antiga {} não encontrada no sistema de arquivos para remoção", oldFileName);
                }
            }

            String originalFilename = file.getOriginalFilename();
            String fileName = UUID.randomUUID() + "_" + originalFilename;
            Path uploadPath = Paths.get("/uploads/animais/");
            if (!Files.exists(uploadPath)) {
                logger.info("Diretório de upload não existe. Criando diretório: {}", uploadPath);
                Files.createDirectories(uploadPath);
            }
            Path filePath = uploadPath.resolve(fileName);
            logger.info("Salvando novo arquivo de imagem '{}' para o animal ID {} no caminho: {}", originalFilename, id, filePath);
            Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
            String imageUrl = "/uploads/animais/" + fileName;

            animal.setUrlImagem(imageUrl);
            animalRepository.save(animal);

            logger.info("Nova imagem salva com sucesso para o animal ID {}. URL: {}", id, imageUrl);
            return imageUrl;
        } catch (IOException e) {
            logger.error("Erro de I/O ao processar upload de imagem para o animal ID {}: {}", id, e.getMessage(), e);
            throw e;
        }
    }

}
