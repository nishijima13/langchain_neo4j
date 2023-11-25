# LangChainのNeo4j QAチュートリアル

以下のチュートリアルを試す。  
https://python.langchain.com/docs/use_cases/graph/graph_cypher_qa/

## 環境構築

Dockerコンテナを起動する。  
```bash
cd 01_turtorial
docker-compose up -d
```

Neo4jのWeb画面にアクセスする。  
http://localhost:7474/browser/  

Web画面上で以下を入力  
Connect to Neo4j  
* Connect URL: neo4j://localhost:7687
* Database: 空白
* Authentication Type: Username / Password
* Username: neo4j
* Password: pleaseletmein

ログインID:neo4j、パスワード:pleaseletmeinでログインする。  
ログインIDやパスワードは[neo4j_docker/Dockerfile](neo4j_docker/Dockerfile)の以下で指定している。
```Dockerfile
ENV NEO4J_AUTH=neo4j/pleaseletmein  
```

## 実行

```bash
# Dockerコンテナに入る
docker exec -it python_docker bash
# OpenAI APIキーを設定
export OPENAI_API_KEY="..."

# チュートリアルを実行
python3 src/demo.py

> Entering new GraphCypherQAChain chain...
Generated Cypher:
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie {name: 'Top Gun'})
RETURN a.name
Full Context:
[{'a.name': 'Tom Cruise'}, {'a.name': 'Val Kilmer'}, {'a.name': 'Anthony Edwards'}, {'a.name': 'Meg Ryan'}]

> Finished chain.
Tom Cruise, Val Kilmer, Anthony Edwards, and Meg Ryan played in Top Gun.
```
