from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from langchain.graphs import Neo4jGraph

# GraphDB接続
graph = Neo4jGraph(url="neo4j://neo4j:7687", username="neo4j", password="pleaseletmein")

# データ削除
graph.query("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")

# ノード作成
# 1. "Top Gun"という名前のMovieノードを作成
# 2. ["Tom Cruise", "Val Kilmer", "Anthony Edwards", "Meg Ryan"]のリストの各要素をActorノードとして作成
# 3. ActorノードとMovieノードをACTED_INの関係で結合
graph.query(
    """
    MERGE (m:Movie {name:"Top Gun"})
    WITH m
    UNWIND ["Tom Cruise", "Val Kilmer", "Anthony Edwards", "Meg Ryan"] AS actor
    MERGE (a:Actor {name:actor})
    MERGE (a)-[:ACTED_IN]->(m)
    """
)
# スキーマの更新
graph.refresh_schema()

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True
)

# チェーンの実行
response = chain.run("Who played in Top Gun?")
print(response)
