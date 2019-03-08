from model.DTO.ProdutoDTO import ProdutoDTO
from model.DAO.ProdutoDAO import ProdutoDAO

class ProdutoCTR:

    def cadastrarProduto(nome, valor):
        produtoDTO = ProdutoDTO()
        produtoDTO.Nome = nome
        produtoDTO.Valor = valor

        produtoDAO = ProdutoDAO
        produtoDAO.cadastrarProduto(produtoDTO)
