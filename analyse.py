from database import Database
from writeAJson import writeAJson


class ProductAnalyzer:
    def __init__(self, database: Database):
        self.db = database

    def totalVendasDia(self):
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$data_compra", "compras": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"_id": 1}},
        ])
        writeAJson(result, "Total_vendas_dia")

    def produtoMaisVendidoTotal(self):
        result = self.db.collection.aggregate([
           {"$unwind": "$produtos"},
           {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
           {"$sort": {"total": -1}},
           {"$limit": 1}
        ])
        writeAJson(result, "Produto_mais_vendido_total")

    def clienteMaisGastouCompra(self):
        # Cliente que mais comprou em cada dia:
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": {"cliente": "$cliente_id", "data": "$data_compra"},
                        "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ])
        writeAJson(result, "Cliente_mais_gastou_uma_compra")

    def produtosVendidosUmPouco(self):
        result = self.db.collection.aggregate([
           {"$unwind": "$produtos"},
           {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
           {"$project": {"comprado_mais_de_um": {"$gt": ["$total", 1]}}},
           {"$match": {"comprado_mais_de_um": True}},
           {"$project": {"_id": "$_id"}}
        ])
        writeAJson(result, "Produtos_vendidos_Pelo_Menos_Uma_Vez")

