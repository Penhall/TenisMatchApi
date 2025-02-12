// /frontend/src/utils/validation.js

/**
 * Valida um arquivo CSV
 * @param {File} file - Arquivo a ser validado
 * @returns {{ isValid: boolean, error?: string }} Resultado da validação
 */
export const validateCSVFile = (file) => {
  if (!file) {
    return { isValid: false, error: 'Nenhum arquivo selecionado' };
  }

  // Validar tipo do arquivo
  if (!file.type && !file.name.endsWith('.csv')) {
    return { 
      isValid: false, 
      error: 'Formato inválido. Apenas arquivos CSV são aceitos' 
    };
  }

  // Validar tamanho (max 10MB)
  const maxSize = 10 * 1024 * 1024; // 10MB em bytes
  if (file.size > maxSize) {
    return { 
      isValid: false, 
      error: 'Arquivo muito grande. Tamanho máximo: 10MB' 
    };
  }

  return { isValid: true };
};

/**
 * Valida os dados do tênis
 * @param {Object} data - Dados do tênis
 * @returns {{ isValid: boolean, errors: Object }} Resultado da validação
 */
export const validateTenisData = (data) => {
  const errors = {};
  
  // Validar estilo
  const validStyles = ['ESP', 'CAS', 'VIN', 'SOC', 'FAS'];
  if (!validStyles.includes(data.tenis_estilo)) {
    errors.tenis_estilo = 'Estilo inválido';
  }

  // Validar marca
  const validBrands = ['Nike', 'Adidas', 'Vans', 'Converse', 'New Balance'];
  if (!validBrands.includes(data.tenis_marca)) {
    errors.tenis_marca = 'Marca inválida';
  }

  // Validar cores
  const validColors = ['BLK', 'WHT', 'COL', 'NEU'];
  if (!validColors.includes(data.tenis_cores)) {
    errors.tenis_cores = 'Cor inválida';
  }

  // Validar preço
  if (!data.tenis_preco || data.tenis_preco <= 0) {
    errors.tenis_preco = 'Preço deve ser maior que zero';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

/**
 * Valida as métricas do modelo
 * @param {Object} metrics - Métricas do modelo
 * @returns {boolean} Se as métricas são válidas
 */
export const validateModelMetrics = (metrics) => {
  if (!metrics) return false;

  const requiredMetrics = [
    'accuracy',
    'precision',
    'recall',
    'f1_score'
  ];

  // Verificar se todas as métricas existem
  const hasAllMetrics = requiredMetrics.every(
    metric => typeof metrics[metric] === 'number'
  );

  // Verificar se os valores estão entre 0 e 1
  const validValues = requiredMetrics.every(
    metric => metrics[metric] >= 0 && metrics[metric] <= 1
  );

  return hasAllMetrics && validValues;
};

/**
 * Valida coluna do CSV
 * @param {Array} headers - Cabeçalhos do CSV
 * @returns {{ isValid: boolean, error?: string }} Resultado da validação
 */
export const validateCSVColumns = (headers) => {
  const requiredColumns = [
    'tenis_estilo',
    'tenis_marca',
    'tenis_cores',
    'tenis_preco',
    'match_success'
  ];

  const missingColumns = requiredColumns.filter(
    col => !headers.includes(col)
  );

  if (missingColumns.length > 0) {
    return {
      isValid: false,
      error: `Colunas obrigatórias faltando: ${missingColumns.join(', ')}`
    };
  }

  return { isValid: true };
};

/**
 * Valida formato do CSV após parse
 * @param {Array} data - Dados do CSV parseado
 * @returns {{ isValid: boolean, errors: Array }} Resultado da validação
 */
export const validateCSVData = (data) => {
  const errors = [];

  data.forEach((row, index) => {
    const { isValid, errors: rowErrors } = validateTenisData(row);
    if (!isValid) {
      errors.push({
        row: index + 1,
        errors: rowErrors
      });
    }
  });

  return {
    isValid: errors.length === 0,
    errors
  };
};