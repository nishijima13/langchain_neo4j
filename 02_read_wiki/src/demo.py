import wikipedia
from langchain import LLMChain, PromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from langchain.graphs import Neo4jGraph

wikipedia.set_lang("ja")

# Wikipediaから藤本タツキのwiki要約を取得
target = "藤本タツキ"

title = wikipedia.search(target)[0]
wp = wikipedia.page(title)
wiki_content = wp.summary

print("### {0}のwiki要約 ###".format(target))
print(wiki_content)
print("#" * 50)
print()

# OpenAIのチャットモデルを定義
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# プロンプトのテンプレート文章を定義
template = """
以下の文章からグラフを作成するCypherクエリのみを出力して下さい。
ただし[:is a]の関係は[:is_a]のように_を含む形で出力して下さい。
{graph_elements}
"""

# テンプレート文章にあるチェック対象の単語を変数化
prompt = PromptTemplate(
    input_variables=["graph_elements"],
    template=template,
)

# OpenAIのAPIにこのプロンプトを送信するためのチェーンを作成
chain = LLMChain(llm=chat, prompt=prompt, verbose=True)
cryptic = chain(wiki_content)["text"]

# チェーンを実行し、結果を表示
print("### {0}の要約からCypherクエリを生成 ###".format(target))
print(cryptic)
print("#" * 50)
print()

# Cypherクエリを実行し、グラフを作成
# GraphDB接続
graph = Neo4jGraph(url="neo4j://neo4j:7687", username="neo4j", password="pleaseletmein")

# データ削除
graph.query("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")

# Cypherクエリを実行
graph.query(cryptic)
# スキーマの更新
graph.refresh_schema()

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0.5), graph=graph, verbose=True
)

# チェーンの実行
print("### {0}に関する質問に対する回答 ###".format(target))
question = "藤本タツキは何者ですか？"
response = chain.run(question)
print("Q: {0}".format(question))
print("A: {0}".format(response))
print("#" * 50)
