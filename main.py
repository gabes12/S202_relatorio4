from database import Database
from analyse import ProductAnalyzer

db = Database(database="mercado", collection="compras")
db.resetDatabase()

products = ProductAnalyzer(db)
products.totalVendasDia()
products.produtoMaisVendidoTotal()
products.clienteMaisGastouCompra()
products.produtosVendidosUmPouco()
