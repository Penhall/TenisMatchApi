// /frontend/src/utils/format.js

/**
 * Formata um número como porcentagem
 * @param {number} value - Valor entre 0 e 1
 * @param {number} decimals - Número de casas decimais
 * @returns {string} Valor formatado como porcentagem
 */
export const formatPercent = (value, decimals = 1) => {
  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * Formata um valor monetário em reais
 * @param {number} value - Valor em reais
 * @returns {string} Valor formatado em BRL
 */
export const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

/**
 * Formata uma data ISO para formato local
 * @param {string} isoDate - Data em formato ISO
 * @returns {string} Data formatada
 */
export const formatDate = (isoDate) => {
  return new Date(isoDate).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * Formata bytes para uma unidade legível
 * @param {number} bytes - Tamanho em bytes
 * @returns {string} Tamanho formatado
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Formata um nome de arquivo para exibição
 * @param {string} filename - Nome do arquivo
 * @param {number} maxLength - Tamanho máximo
 * @returns {string} Nome formatado
 */
export const formatFileName = (filename, maxLength = 20) => {
  if (filename.length <= maxLength) return filename
  const extension = filename.split('.').pop()
  const name = filename.substring(0, filename.lastIndexOf('.'))
  const truncated = name.substring(0, maxLength - extension.length - 3)
  return `${truncated}...${extension}`
}

/**
 * Formata um erro para exibição ao usuário
 * @param {Error|string} error - Erro ou mensagem de erro
 * @returns {string} Mensagem formatada
 */
export const formatError = (error) => {
  if (typeof error === 'string') return error
  if (error.response?.data?.detail) return error.response.data.detail
  if (error.message) return error.message
  return 'Ocorreu um erro inesperado'
}