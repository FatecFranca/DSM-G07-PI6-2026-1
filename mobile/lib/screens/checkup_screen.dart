import 'package:PetDex/data/enums/input_size.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:PetDex/theme/app_theme.dart';
import 'package:PetDex/components/ui/disease_prediction.dart';
import 'package:PetDex/components/ui/yes_or_no_question.dart';
import 'package:PetDex/components/ui/input.dart';
import 'package:PetDex/components/ui/button.dart';
import 'package:PetDex/services/animal_service.dart';
import 'package:PetDex/main.dart';
import 'package:PetDex/models/animal.dart';

class CheckupScreen extends StatefulWidget {
  const CheckupScreen({super.key});

  @override
  State<CheckupScreen> createState() => _CheckupScreenState();
}

class _CheckupScreenState extends State<CheckupScreen> {
  final AnimalService _animalService = AnimalService();
  final petNome = authService.getPetName();
  bool _mostrouIntroducao =
      false; // Controla se a tela de introdução foi exibida
  int _etapaAtual = 0; // 0..5 perguntas, 6 = resultado
  bool _enviando = false;
  bool _mostrouResultado = false;
  String? _resultadoRotulo; // Texto apresentado no DiseasePrediction\
  String? _description;

  bool _exibindoCheckupGeral = true;
  Animal? _animal;
  Map<String, dynamic>? _recomendacao;
  Map<String, dynamic>? _pesoIdealData;
  bool _carregandoAnimal = true;
  bool _carregandoRecomendacao = true;
  String? _erroCarregamento;

  double calcularPesoIdeal(double peso) {
    return peso * 0.91;
  }

  double calcularPesoMinimo(double pesoIdeal) {
    return pesoIdeal * 0.85;
  }

  double calcularPesoMaximo(double pesoIdeal) {
    return pesoIdeal * 1.15;
  }

  Future<void> _carregarDados() async {
    setState(() {
      _carregandoAnimal = true;
      _carregandoRecomendacao = true;
      _erroCarregamento = null;
    });

    final animalId = authService.getAnimalId();
    if (animalId == null || animalId.isEmpty) {
      setState(() {
        _erroCarregamento = 'ID do pet não encontrado.';
        _carregandoAnimal = false;
        _carregandoRecomendacao = false;
      });
      return;
    }

    try {
      final animal = await _animalService.getAnimalInfo(animalId);
      
      setState(() {
        _animal = animal;
        _carregandoAnimal = false;
      });

      // 1. Carrega dados de Peso Ideal primeiro
      final pesoIdealMap = await _animalService.getPesoIdeal(animalId);
      setState(() {
        _pesoIdealData = pesoIdealMap;
      });

      final double pesoIdealVal = (pesoIdealMap['peso_ideal'] as num).toDouble();

      // 2. Carrega recomendação com base no peso ideal obtido
      final rec = await _animalService.getIaRecomendacao(animalId, pesoIdealVal);
      setState(() {
        _recomendacao = rec;
        _carregandoRecomendacao = false;
      });
    } catch (e) {
      print('Erro ao carregar dados do checkup: $e');
      setState(() {
        _erroCarregamento = 'Erro de conexão com a API.';
        _carregandoAnimal = false;
        _carregandoRecomendacao = false;
      });
    }
  }

  String getRacaoAssetPath(String brand) {
    final clean = brand.toLowerCase();
    if (clean.contains('royal canin')) {
      return 'assets/images/racao-royal-canin.png';
    }
    if (clean.contains('blue buffalo')) {
      return 'assets/images/racao-blue-buffalo.png';
    }
    if (clean.contains('purina')) {
      return 'assets/images/racao-purina.png';
    }
    if (clean.contains('pedigree')) {
      return 'assets/images/racao-pedigree.png';
    }
    if (clean.contains('hill') || clean.contains('science diet')) {
      return 'assets/images/racao-hills.png';
    }
    if (clean.contains('nutrience')) {
      return 'assets/images/racao-nutrience.png';
    }
    if (clean.contains('authority')) {
      return 'assets/images/racao-authority.png';
    }
    if (clean.contains('iams')) {
      return 'assets/images/racao-iams.png';
    }
    if (clean.contains('nutro')) {
      return 'assets/images/racao-nutro.png';
    }
    if (clean.contains('special')) {
      return 'assets/images/racao-special.png';
    }
    if (clean.contains('wellness')) {
      return 'assets/images/racao-wellness.png';
    }
    if (clean.contains('natural balance')) {
      return 'assets/images/racao-natural-balance.png';
    }
    return 'assets/images/racao-generica.png';
  }

  final TextEditingController _duracaoController = TextEditingController(
    text: '0',
  );
  final ScrollController _scrollController = ScrollController();
  final FocusNode _duracaoFocusNode = FocusNode();
  final GlobalKey _duracaoInputKey = GlobalKey();

  // Respostas dos 34 campos (duracao = int em dias, demais 0/1)
  late Map<String, dynamic> respostas;

  @override
  void initState() {
    super.initState();
    _resetarFluxo();
    _carregarDados();

    // Listener para rolar a tela quando o input de duração receber foco
    _duracaoFocusNode.addListener(() {
      if (_duracaoFocusNode.hasFocus) {
        _scrollToInput();
      }
    });
  }

  void _scrollToInput() {
    // Aguarda o teclado aparecer e a renderização completar
    Future.delayed(const Duration(milliseconds: 400), () {
      if (!mounted) return;
      if (!_scrollController.hasClients) return;

      final inputContext = _duracaoInputKey.currentContext;
      if (inputContext == null) return;

      // Obtém a posição do Input na tela
      final RenderBox? renderBox =
          inputContext.findRenderObject() as RenderBox?;
      if (renderBox == null) return;

      // Posição do Input relativa ao topo da tela
      final position = renderBox.localToGlobal(Offset.zero);
      final inputHeight = renderBox.size.height;

      // Altura do teclado (aproximadamente)
      final keyboardHeight = MediaQuery.of(context).viewInsets.bottom;

      // Altura visível da tela (sem o teclado)
      final screenHeight = MediaQuery.of(context).size.height;
      final visibleHeight = screenHeight - keyboardHeight;

      // Calcula onde o Input deve estar (centralizado na área visível)
      final targetPosition =
          position.dy - (visibleHeight / 2) + (inputHeight / 2);

      // Scroll atual
      final currentScroll = _scrollController.offset;

      // Nova posição de scroll
      final newScroll =
          currentScroll +
          targetPosition -
          100; // -100 para dar um espaço extra no topo

      // Anima para a nova posição
      _scrollController.animateTo(
        newScroll.clamp(0.0, _scrollController.position.maxScrollExtent),
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  @override
  void dispose() {
    _duracaoController.dispose();
    _scrollController.dispose();
    _duracaoFocusNode.dispose();
    super.dispose();
  }

  void _resetarFluxo() {
    respostas = {
      'duracao': 0,
      'perda_de_apetite': null,
      'vomito': null,
      'diarreia': null,
      'tosse': null,
      'dificuldade_para_respirar': null,
      'dificuldade_para_locomover': null,
      'problemas_na_pele': null,
      'secrecao_nasal': null,
      'secrecao_ocular': null,
      'agitacao': null,
      'andar_em_circulos': null,
      'aumento_apetite': null,
      'cera_excessiva_nas_orelhas': null,
      'coceira': null,
      'desidratacao': null,
      'desmaio': null,
      'dificuldade_para_urinar': null,
      'dor': null,
      'espamos_musculares': null,
      'espirros': null,
      'febre': null,
      'fraqueza': null,
      'inchaco': null,
      'lambedura': null,
      'letargia': null,
      'lingua_azulada': null,
      'perda_de_pelos': null,
      'perda_de_peso': null,
      'ranger_de_dentes': null,
      'ronco': null,
      'salivacao': null,
      'suor_alterado': null,
    };
    _duracaoController.text = '0';
    _mostrouIntroducao = false; // Volta para a tela de introdução
    _etapaAtual = 0;
    _enviando = false;
    _mostrouResultado = false;
    _resultadoRotulo = null;
    _exibindoCheckupGeral = true;
  }

  // Mapeia os códigos de resultado da API para rótulos amigáveis
  String _mapResultadoParaRotulo(String resultado) {
    switch (resultado) {
      case 'gastrointestinal':
        return 'Problemas gastrointestinais';
      case 'respiratoria':
        return 'Problemas respiratórios';
      case 'cutanea':
        return 'Problemas cutâneos';
      case 'urogenital':
        return 'Problemas urogenitais';
      case 'neuro_musculoesqueletica':
        return 'Problemas neuro-musculoesqueléticos';
      case 'cardiovascular_hematologica':
        return 'Problemas cardiovasculares/hematológicos';
      case 'nenhuma':
      default:
        return '$petNome está saúdavel';
    }
  }

  String _mapResultadoParaRotuloDescricao(String resultado) {
    if (resultado == 'nenhuma') {
      return 'Não foi identificado nenhum problema de saúde';
    }
    return "";
  }

  void _atualizarResposta(String chave, bool? valor) {
    setState(() {
      if (valor == null) {
        respostas[chave] = null; // ainda não respondida
      } else {
        respostas[chave] = valor ? 1 : 0;
      }
    });
  }

  bool? _iv(String chave) {
    final v = respostas[chave];
    if (v == null) return null;
    return v == 1;
  }

  // Retorna as chaves das perguntas para cada etapa
  List<String> _perguntasDaEtapa(int etapa) {
    switch (etapa) {
      case 0:
        return [
          'agitacao',
          'letargia',
          'fraqueza',
          'andar_em_circulos',
          'ranger_de_dentes',
          'lambedura',
        ];
      case 1:
        return [
          'perda_de_apetite',
          'aumento_apetite',
          'vomito',
          'diarreia',
          'perda_de_peso',
          'desidratacao',
        ];
      case 2:
        return [
          'tosse',
          'dificuldade_para_respirar',
          'ronco',
          'espirros',
          'lingua_azulada',
          'febre',
        ];
      case 3:
        return [
          'dificuldade_para_locomover',
          'dor',
          'espamos_musculares',
          'desmaio',
          'inchaco',
        ];
      case 4:
        return [
          'problemas_na_pele',
          'coceira',
          'perda_de_pelos',
          'cera_excessiva_nas_orelhas',
          'suor_alterado',
          'salivacao',
        ];
      case 5:
        return ['secrecao_nasal', 'secrecao_ocular', 'dificuldade_para_urinar'];
      default:
        return [];
    }
  }

  // Verifica se todas as perguntas da etapa atual foram respondidas
  bool _todasPerguntasRespondidas() {
    final perguntas = _perguntasDaEtapa(_etapaAtual);
    for (final chave in perguntas) {
      if (respostas[chave] == null) {
        return false;
      }
    }
    return true;
  }

  Widget _telaIntroducao() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        const SizedBox(height: 20),
        // Título Principal
        Text(
          'Checkup Inteligente',
          textAlign: TextAlign.center,
          style: GoogleFonts.poppins(
            color: AppColors.orange,
            fontSize: 28,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 4),
        // Subtítulo
        Text(
          'Descubra o que o seu pet pode estar sentindo',
          textAlign: TextAlign.center,
          style: GoogleFonts.poppins(
            color: AppColors.orange900,
            fontSize: 12,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: 24),
        // Parágrafo Explicativo
        Text(
          'Responda algumas perguntas rápidas sobre os sintomas observados e deixe a inteligência da PetDex analisar os dados para identificar possíveis problemas de saúde.',
          textAlign: TextAlign.center,
          style: GoogleFonts.poppins(
            color: AppColors.brown,
            fontSize: 14,
            fontWeight: FontWeight.w400,
            height: 1.5,
          ),
        ),
        const SizedBox(height: 32),
        // Card Informativo
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: AppColors.sand,
            borderRadius: BorderRadius.circular(24.0),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Título do Card
              Text(
                'A nossa análise poderá indicar se há sinais relacionados a:',
                textAlign: TextAlign.center,
                style: GoogleFonts.poppins(
                  color: AppColors.orange900,
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 16),
              // Lista de itens
              _buildListItem('Sistema cardiovascular e hematológico'),
              _buildListItem('Problemas de pele (cutâneas)'),
              _buildListItem('Distúrbios gastrointestinais'),
              _buildListItem('Problemas neurológicos ou musculoesqueléticos'),
              _buildListItem('Alterações respiratórias'),
              _buildListItem('Condições do trato urinário ou genital'),
              const SizedBox(height: 16),
              // Texto adicional
              Center(
                child: Text(
                  'Ou indicar que está tudo bem! 🐾',
                  textAlign: TextAlign.center,
                  style: GoogleFonts.poppins(
                    color: AppColors.orange900,
                    fontSize: 14,
                    fontWeight: FontWeight.normal,
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 32),
        // Botão de Ação
        Button(
          text: 'Iniciar',
          onPressed: () {
            setState(() {
              _mostrouIntroducao = true;
            });
            // Rola para o topo quando iniciar
            WidgetsBinding.instance.addPostFrameCallback((_) {
              if (_scrollController.hasClients) {
                _scrollController.animateTo(
                  0,
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.easeOut,
                );
              }
            });
          },
        ),
        const SizedBox(height: 12),
        TextButton(
          onPressed: () {
            setState(() {
              _exibindoCheckupGeral = true;
            });
          },
          child: Text(
            'Voltar ao Dashboard',
            style: GoogleFonts.poppins(
              color: AppColors.orange900,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
        const SizedBox(height: 16),
        // Disclaimer
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Text(
            'Essa análise tem caráter informativo e não substitui a avaliação de um médico veterinário.',
            textAlign: TextAlign.center,
            style: GoogleFonts.poppins(
              color: AppColors.brown.withOpacity(0.6),
              fontSize: 12,
              fontWeight: FontWeight.w400,
              height: 1.4,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildListItem(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '• ',
            style: GoogleFonts.poppins(
              color: AppColors.brown,
              fontSize: 14,
              fontWeight: FontWeight.w600,
            ),
          ),
          Expanded(
            child: Text(
              text,
              style: GoogleFonts.poppins(
                color: AppColors.brown,
                fontSize: 14,
                fontWeight: FontWeight.w400,
                height: 1.4,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _tituloTopo() {
    if (_exibindoCheckupGeral) {
      return const SizedBox.shrink();
    }
    // Não mostra título na tela de introdução
    if (!_mostrouIntroducao) {
      return const SizedBox.shrink();
    }

    String titulo;
    if (_mostrouResultado) {
      titulo = 'Resultado da Análise';
    } else {
      switch (_etapaAtual) {
        case 0:
          titulo = 'Comportamento e Rotina';
          break;
        case 1:
          titulo = 'Alimentação e Digestão';
          break;
        case 2:
          titulo = 'Respiração e Circulação';
          break;
        case 3:
          titulo = 'Movimento e Coordenação';
          break;
        case 4:
          titulo = 'Pele, Orelhas e Pelos';
          break;
        case 5:
        default:
          titulo = 'Sintomas Específicos';
      }
    }
    return Column(
      children: [
        Text(
          titulo,
          style: GoogleFonts.poppins(
            color: AppColors.orange,
            fontSize: 22,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
      ],
    );
  }

  Widget _etapa1() {
    return Column(
      children: [
        YesOrNoQuestion(
          questionText: '$petNome está agitado ou mais inquieto que o normal?',
          initialValue: _iv('agitacao'),
          onChanged: (v) => _atualizarResposta('agitacao', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Você notou letargia?',
          descriptionQuestion: 'Desânimo, cansaço ou dorme mais que o normal',
          initialValue: _iv('letargia'),
          onChanged: (v) => _atualizarResposta('letargia', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText:
              '$petNome demonstra fraqueza ou dificuldade em se levantar?',
          initialValue: _iv('fraqueza'),
          onChanged: (v) => _atualizarResposta('fraqueza', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Está andando em círculos, sem motivo aparente?',
          initialValue: _iv('andar_em_circulos'),
          onChanged: (v) => _atualizarResposta('andar_em_circulos', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Está rangendo os dentes com frequência?',
          initialValue: _iv('ranger_de_dentes'),
          onChanged: (v) => _atualizarResposta('ranger_de_dentes', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText:
              'Apresenta lambedura excessiva em alguma parte do corpo?',
          initialValue: _iv('lambedura'),
          onChanged: (v) => _atualizarResposta('lambedura', v),
        ),
      ],
    );
  }

  Widget _etapa2() {
    return Column(
      children: [
        YesOrNoQuestion(
          questionText: '$petNome perdeu o apetite recentemente?',
          initialValue: _iv('perda_de_apetite'),
          onChanged: (v) => _atualizarResposta('perda_de_apetite', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Houve aumento no apetite, comendo mais que o normal?',
          initialValue: _iv('aumento_apetite'),
          onChanged: (v) => _atualizarResposta('aumento_apetite', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Está vomitando com frequência?',
          initialValue: _iv('vomito'),
          onChanged: (v) => _atualizarResposta('vomito', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Apresenta diarreia ou fezes muito moles?',
          initialValue: _iv('diarreia'),
          onChanged: (v) => _atualizarResposta('diarreia', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Você notou perda de peso sem motivo aparente?',
          initialValue: _iv('perda_de_peso'),
          onChanged: (v) => _atualizarResposta('perda_de_peso', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: '$petNome está com sinais de desidratação?',
          descriptionQuestion:
              ' Boca, olhos ou nariz secos, urina escura e em menor quantidade, boca quente.',
          initialValue: _iv('desidratacao'),
          onChanged: (v) => _atualizarResposta('desidratacao', v),
        ),
      ],
    );
  }

  Widget _etapa3() {
    return Column(
      children: [
        YesOrNoQuestion(
          questionText: '$petNome está com tosse?',
          initialValue: _iv('tosse'),
          onChanged: (v) => _atualizarResposta('tosse', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText:
              'Tem dificuldade para respirar ou respiração ofegante em repouso?',
          initialValue: _iv('dificuldade_para_respirar'),
          onChanged: (v) => _atualizarResposta('dificuldade_para_respirar', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Você notou roncos ou barulhos diferentes ao respirar?',
          initialValue: _iv('ronco'),
          onChanged: (v) => _atualizarResposta('ronco', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Está espirrando com frequência?',
          initialValue: _iv('espirros'),
          onChanged: (v) => _atualizarResposta('espirros', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'A língua ou gengivas estão azuladas?',
          initialValue: _iv('lingua_azulada'),
          onChanged: (v) => _atualizarResposta('lingua_azulada', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: '$petNome parece ter febre?',
          descriptionQuestion:
              'Aparenta estar com o corpo mais quente, especialmente as orelhas.',
          initialValue: _iv('febre'),
          onChanged: (v) => _atualizarResposta('febre', v),
        ),
      ],
    );
  }

  Widget _etapa4() {
    return Column(
      children: [
        YesOrNoQuestion(
          questionText: '$petNome tem dificuldade para se locomover?',
          descriptionQuestion: 'Manca ou evita andar?',
          initialValue: _iv('dificuldade_para_locomover'),
          onChanged: (v) => _atualizarResposta('dificuldade_para_locomover', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Demonstra dor ao ser tocado ou ao se mover?',
          initialValue: _iv('dor'),
          onChanged: (v) => _atualizarResposta('dor', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Você percebeu espasmos musculares?',
          descriptionQuestion: 'Tremores involuntários',
          initialValue: _iv('espamos_musculares'),
          onChanged: (v) => _atualizarResposta('espamos_musculares', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: '$petNome já teve algum desmaio recentemente?',
          initialValue: _iv('desmaio'),
          onChanged: (v) => _atualizarResposta('desmaio', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Há inchaços visíveis em alguma parte do corpo?',
          initialValue: _iv('inchaco'),
          onChanged: (v) => _atualizarResposta('inchaco', v),
        ),
      ],
    );
  }

  Widget _etapa5() {
    return Column(
      children: [
        YesOrNoQuestion(
          questionText:
              'Há problemas na pele, como feridas, irritações ou manchas?',
          initialValue: _iv('problemas_na_pele'),
          onChanged: (v) => _atualizarResposta('problemas_na_pele', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: '$petNome está com coceira constante?',
          initialValue: _iv('coceira'),
          onChanged: (v) => _atualizarResposta('coceira', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Há perda de pelos excessiva ou em áreas específicas?',
          initialValue: _iv('perda_de_pelos'),
          onChanged: (v) => _atualizarResposta('perda_de_pelos', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Há cera excessiva nas orelhas ou mau cheiro?',
          initialValue: _iv('cera_excessiva_nas_orelhas'),
          onChanged: (v) => _atualizarResposta('cera_excessiva_nas_orelhas', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Você notou suor alterado?',
          descriptionQuestion: 'Áreas úmidas ou odor incomum',
          initialValue: _iv('suor_alterado'),
          onChanged: (v) => _atualizarResposta('suor_alterado', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Está com salivação maior que o normal?',
          initialValue: _iv('salivacao'),
          onChanged: (v) => _atualizarResposta('salivacao', v),
        ),
      ],
    );
  }

  Widget _etapa6() {
    return Column(
      children: [
        YesOrNoQuestion(
          questionText: 'Há secreção nasal?',
          descriptionQuestion: 'Corrimento pelo nariz',
          initialValue: _iv('secrecao_nasal'),
          onChanged: (v) => _atualizarResposta('secrecao_nasal', v),
        ),
        const SizedBox(height: 16),
        YesOrNoQuestion(
          questionText: 'Há secreção ocular?',
          descriptionQuestion: 'Olhos lacrimejando ou com crostas',
          initialValue: _iv('secrecao_ocular'),
          onChanged: (v) => _atualizarResposta('secrecao_ocular', v),
        ),
        const SizedBox(height: 16),

        YesOrNoQuestion(
          questionText: '$petNome demonstra dificuldade para urinar?',
          initialValue: _iv('dificuldade_para_urinar'),
          onChanged: (v) => _atualizarResposta('dificuldade_para_urinar', v),
        ),
        const SizedBox(height: 24),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 18),
          decoration: BoxDecoration(
            color: AppColors.sand,
            borderRadius: BorderRadius.circular(24.0),
          ),
          child: Text(
            'Qual é a duração dos sintomas?',
            textAlign: TextAlign.center,
            style: GoogleFonts.poppins(
              color: AppColors.orange900,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
        // Duração dos sintomas (dias)
        const SizedBox(height: 2),
        Input(
          key: _duracaoInputKey,
          hintText: '3 ',
          controller: _duracaoController,
          focusNode: _duracaoFocusNode,
          centerText: true,
          suffixText: ' dias',
          size: InputSize.large,
          keyboardType: TextInputType.number,
          onChanged: (text) {
            final n = int.tryParse(text.trim());
            setState(() {
              respostas['duracao'] = n ?? 0;
            });
          },
        ),
      ],
    );
  }

  Future<void> _enviarRespostas() async {
    final animalId = authService.getAnimalId();
    if (animalId == null || animalId.isEmpty) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('ID do pet não encontrado. Faça login novamente.'),
        ),
      );
      return;
    }

    setState(() {
      _enviando = true;
    });

    try {
      print('[CheckupScreen] 📤 Preparando envio de respostas...');
      print('[CheckupScreen] Animal ID: $animalId');
      print('[CheckupScreen] Respostas: $respostas');

      final result = await _animalService.postCheckup(animalId, respostas);
      final rotulo = _mapResultadoParaRotulo(result.resultado);
      final description = _mapResultadoParaRotuloDescricao(result.resultado);
      if (!mounted) return;
      setState(() {
        _description = description;
        _resultadoRotulo = rotulo;
        _mostrouResultado = true;
        _etapaAtual = 6; // etapa de resultado
      });
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_scrollController.hasClients) {
          _scrollController.animateTo(
            0,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Erro ao enviar: $e')));
    } finally {
      if (mounted) {
        setState(() {
          _enviando = false;
        });
      }
    }
  }

  Widget _conteudoPorEtapa() {
    if (_exibindoCheckupGeral) {
      return _buildCheckupGeral();
    }
    // Mostra a tela de introdução se ainda não foi exibida
    if (!_mostrouIntroducao) {
      return _telaIntroducao();
    }

    if (_mostrouResultado) {
      return Column(
        children: [
          DiseasePrediction(
            diseaseText: _resultadoRotulo ?? 'Análise indisponível',
            descriptionText: _description != "" && _description != null
                ? _description
                : null,
          ),
        ],
      );
    }

    switch (_etapaAtual) {
      case 0:
        return _etapa1();
      case 1:
        return _etapa2();
      case 2:
        return _etapa3();
      case 3:
        return _etapa4();
      case 4:
        return _etapa5();
      case 5:
      default:
        return _etapa6();
    }
  }

  String _textoBotao() {
    if (_mostrouResultado) return 'Começar Novamente';
    if (_etapaAtual < 5) return 'Continuar';
    return 'Enviar Respostas';
  }

  // Verifica se pode voltar para a etapa anterior ou para a introdução
  bool _podeVoltar() {
    // Pode voltar se já passou da introdução e não está mostrando resultado
    // Agora permite voltar mesmo na etapa 0 (volta para a introdução)
    return _mostrouIntroducao && _etapaAtual >= 0 && !_mostrouResultado;
  }

  // Volta para a etapa anterior ou para a tela de introdução
  void _voltarEtapa() {
    setState(() {
      if (_etapaAtual == 0) {
        // Se está na primeira etapa, volta para a introdução
        _mostrouIntroducao = false;
      } else {
        // Caso contrário, volta para a etapa anterior
        _etapaAtual--;
      }
    });
    // Rola para o topo quando voltar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          0,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _onPressBotao() {
    if (_mostrouResultado) {
      setState(() {
        _resetarFluxo();
      });
      return;
    }

    // Validar se todas as perguntas foram respondidas antes de continuar
    if (!_todasPerguntasRespondidas()) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text(
            'Por favor, responda todas as perguntas antes de continuar.',
          ),
          backgroundColor: AppColors.orange900,
          behavior: SnackBarBehavior.floating,
          margin: EdgeInsets.only(
            bottom: MediaQuery.of(context).size.height - 150,
            left: 16,
            right: 16,
          ),
          duration: const Duration(seconds: 3),
        ),
      );
      return;
    }

    if (_etapaAtual < 5) {
      setState(() {
        _etapaAtual += 1;
      });
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_scrollController.hasClients) {
          _scrollController.animateTo(
            0,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      });
    } else {
      _enviarRespostas();
    }
  }

  @override
  Widget build(BuildContext context) {
    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: SafeArea(
        child: SingleChildScrollView(
          controller: _scrollController,
          padding: EdgeInsets.fromLTRB(
            26,
            12,
            26,
            bottomInset > 0
                ? bottomInset + 40
                : 280.0,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 6),
              _tituloTopo(),
              const SizedBox(height: 16),

              _conteudoPorEtapa(),

              // Esconde o botão na tela de introdução (ela tem seu próprio botão)
              if (_mostrouIntroducao) ...[
                const SizedBox(height: 28),
                Button(
                  text: _enviando ? 'Enviando...' : _textoBotao(),
                  onPressed: _enviando ? () {} : _onPressBotao,
                ),
                // Botão Voltar - aparece quando pode voltar
                if (_podeVoltar()) ...[
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: _voltarEtapa,
                    style: TextButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.arrow_back,
                          size: 18,
                          color: AppColors.orange900,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'Voltar',
                          style: GoogleFonts.poppins(
                            color: AppColors.orange900,
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
                const SizedBox(height: 20),
                if (_enviando)
                  const CircularProgressIndicator(color: AppColors.orange900),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCheckupGeral() {
    if (_carregandoAnimal) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.symmetric(vertical: 60.0),
          child: CircularProgressIndicator(color: AppColors.orange900),
        ),
      );
    }

    if (_erroCarregamento != null || _animal == null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              Text(
                _erroCarregamento ?? 'Erro ao carregar dados do pet.',
                style: GoogleFonts.poppins(color: Colors.red, fontSize: 16),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _carregarDados,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.orange900,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
                child: const Text('Tentar Novamente', style: TextStyle(color: Colors.white)),
              ),
            ],
          ),
        ),
      );
    }

    final animal = _animal!;
    final pesoIdeal = (_pesoIdealData?['peso_ideal'] as num?)?.toDouble() ?? calcularPesoIdeal(animal.peso);
    final pesoMinimo = (_pesoIdealData?['peso_minimo'] as num?)?.toDouble() ?? calcularPesoMinimo(pesoIdeal);
    final pesoMaximo = (_pesoIdealData?['peso_maximo'] as num?)?.toDouble() ?? calcularPesoMaximo(pesoIdeal);
    final currentW = (_pesoIdealData?['peso_atual'] as num?)?.toDouble() ?? animal.peso;

    // Calcula a posição proporcional
    double range = pesoMaximo - pesoMinimo;
    double pct = range > 0 ? (currentW - pesoMinimo) / range : 0.5;
    pct = pct.clamp(0.02, 0.98); // safe limits between 2% and 98%

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const SizedBox(height: 12),
        // Título Principal
        Text(
          'Checkup Gerais',
          textAlign: TextAlign.center,
          style: GoogleFonts.poppins(
            color: AppColors.orange,
            fontSize: 28,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 4),
        // Subtítulo
        Text(
          'Peso ideal para seu pet é de ${pesoIdeal.toStringAsFixed(2)}kg',
          textAlign: TextAlign.center,
          style: GoogleFonts.poppins(
            color: AppColors.brown,
            fontSize: 15,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 32),

        // Termômetro de Peso
        Column(
          children: [
            // Barra de Gradiente de Peso
            Container(
              height: 26,
              width: double.infinity,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(13),
                gradient: const LinearGradient(
                  colors: [
                    Color(0xFFD32F2F), // Red
                    Color(0xFFF39200), // Orange
                    Color(0xFF388E3C), // Green
                    Color(0xFF388E3C), // Green
                    Color(0xFFF39200), // Orange
                    Color(0xFFD32F2F), // Red
                  ],
                  stops: [0.0, 0.15, 0.35, 0.65, 0.85, 1.0],
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 4,
                    offset: const Offset(0, 2),
                  )
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(left: 16.0),
                    child: Text(
                      '${pesoMinimo.toStringAsFixed(2)}kg',
                      style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                    ),
                  ),
                  Text(
                    '${pesoIdeal.toStringAsFixed(2)}kg',
                    style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                  Padding(
                    padding: const EdgeInsets.only(right: 16.0),
                    child: Text(
                      '${pesoMaximo.toStringAsFixed(2)}kg',
                      style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 6),
            Container(
              width: double.infinity,
              height: 40,
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final width = constraints.maxWidth;
                  const containerWidth = 120.0;
                  final leftOffset = pct * width - (containerWidth / 2);
                  return Stack(
                    clipBehavior: Clip.none,
                    children: [
                      Positioned(
                        left: leftOffset.clamp(0.0, width - containerWidth),
                        top: 0,
                        child: Container(
                          width: containerWidth,
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              // Linha indicadora vertical
                              Container(
                                width: 3,
                                height: 8,
                                decoration: BoxDecoration(
                                  color: AppColors.orange900,
                                  borderRadius: BorderRadius.circular(1.5),
                                ),
                              ),
                              const SizedBox(height: 4),
                              // Texto de Peso Atual
                              Text(
                                'Seu pet pesa ${currentW.toInt() == currentW ? currentW.toInt() : currentW}kg',
                                textAlign: TextAlign.center,
                                style: GoogleFonts.poppins(
                                  color: AppColors.orange900,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  );
                },
              ),
            ),
          ],
        ),
        const SizedBox(height: 20),

        // Título Ração
        Text(
          'Conheça a ração ideal para uma refeição balanceada',
          textAlign: TextAlign.center,
          style: GoogleFonts.poppins(
            color: AppColors.orange900,
            fontSize: 15,
            fontWeight: FontWeight.w800,
          ),
        ),
        const SizedBox(height: 16),

        // Card Amarelo da Ração
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: AppColors.sand,
            borderRadius: BorderRadius.circular(24.0),
          ),
          child: _carregandoRecomendacao
              ? const Center(
                  child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 20.0),
                    child: CircularProgressIndicator(color: AppColors.orange900),
                  ),
                )
              : _buildRecomendacaoCard(),
        ),
        const SizedBox(height: 32),

        // Botão Checar Saúde
        Button(
          text: 'Checar saúde',
          onPressed: () {
            setState(() {
              _exibindoCheckupGeral = false;
            });
          },
        ),
        const SizedBox(height: 12),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Text(
            'Responda algumas perguntas rápidas sobre os sintomas observados e deixe a inteligência da PetDex analisar os dados para identificar possíveis problemas de saúde.',
            textAlign: TextAlign.center,
            style: GoogleFonts.poppins(
              fontSize: 12,
              height: 1.5,
              color: AppColors.brown.withOpacity(0.7),
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildRecomendacaoCard() {
    if (_recomendacao == null) {
      return Text(
        'Não foi possível gerar a recomendação no momento.',
        style: GoogleFonts.poppins(color: AppColors.brown, fontSize: 14),
      );
    }

    final sugeridos = _recomendacao!['sugestoes_racao'] as List<dynamic>?;
    if (sugeridos == null || sugeridos.isEmpty) {
      return Text(
        'Nenhuma ração recomendada encontrada.',
        style: GoogleFonts.poppins(color: AppColors.brown, fontSize: 14),
      );
    }

    final firstRacao = sugeridos[0];
    final hasAlt = sugeridos.length > 1;
    final altRacao = hasAlt ? sugeridos[1] : null;

    String firstRacaoName = "";
    String firstRacaoMarca = "";
    String firstRacaoMotivo = "";

    if (firstRacao is Map) {
      firstRacaoName = firstRacao['nome'] ?? '';
      firstRacaoMarca = firstRacao['marca'] ?? '';
      firstRacaoMotivo = firstRacao['motivo'] ?? '';
    } else {
      firstRacaoName = firstRacao.toString();
    }

    String altRacaoName = "";
    if (altRacao != null) {
      if (altRacao is Map) {
        altRacaoName = altRacao['nome'] ?? altRacao['marca'] ?? '';
      } else {
        altRacaoName = altRacao.toString();
      }
    }

    final assetPath = getRacaoAssetPath(firstRacaoName.isNotEmpty ? firstRacaoName : firstRacaoMarca);

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Imagem da ração
        ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: Container(
            width: 115,
            height: 115,
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.brown.withOpacity(0.1)),
            ),
            child: Image.asset(
              assetPath,
              fit: BoxFit.contain,
            ),
          ),
        ),
        const SizedBox(width: 16),
        // Detalhes da recomendação
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (firstRacaoMarca.isNotEmpty)
                Text.rich(
                  TextSpan(
                    children: [
                      const TextSpan(
                        text: 'Marca: ',
                        style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.orange900),
                      ),
                      TextSpan(
                        text: firstRacaoMarca,
                        style: const TextStyle(fontWeight: FontWeight.w600, color: AppColors.brown),
                      ),
                    ],
                  ),
                  style: GoogleFonts.poppins(fontSize: 14),
                ),
              if (firstRacaoName.isNotEmpty) ...[
                const SizedBox(height: 4),
                Text.rich(
                  TextSpan(
                    children: [
                      const TextSpan(
                        text: 'Nome: ',
                        style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.orange900),
                      ),
                      TextSpan(
                        text: firstRacaoName,
                        style: const TextStyle(fontWeight: FontWeight.w600, color: AppColors.brown),
                      ),
                    ],
                  ),
                  style: GoogleFonts.poppins(fontSize: 14),
                ),
              ],
              if (firstRacaoMotivo.isNotEmpty) ...[
                const SizedBox(height: 8),
                Divider(color: AppColors.brown.withOpacity(0.1), height: 1),
                const SizedBox(height: 6),
                Text.rich(
                  TextSpan(
                    children: [
                      const TextSpan(
                        text: 'Motivo: ',
                        style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.orange900),
                      ),
                      TextSpan(
                        text: firstRacaoMotivo,
                        style: const TextStyle(fontStyle: FontStyle.italic, color: AppColors.brown),
                      ),
                    ],
                  ),
                  style: GoogleFonts.poppins(fontSize: 12),
                ),
              ],
              if (altRacaoName.isNotEmpty) ...[
                const SizedBox(height: 8),
                Text(
                  'Alternativa: $altRacaoName',
                  style: GoogleFonts.poppins(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: AppColors.brown.withOpacity(0.75),
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }
}
