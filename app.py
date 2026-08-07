import streamlit as st
from langchain_community.document_loaders import TextLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title= 'Jango')
st.title('Jango')
st.write("Jango est votre assistant conversationnel qui répond de façon pertinente et intelligente à vos préocupations.")

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
@st.cache_resource
def load_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=st.secrets["GEMINI_API_KEY"], streaming= True)
@st.cache_resource
def load_vectorstore(chunks, embeddings):
    return FAISS.from_documents(chunks, embeddings)
# ============================================== #
#  configuration de l'historique de conversation 
# ============================================== #
if "messages" not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# ============================================== #
#         configuration du workflow RAG 
# ============================================== #
loader= TextLoader("informations.txt")
documents= loader.load()
text_splitter= RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks= text_splitter.split_documents(documents)
embeddings= load_embeddings()
vectorstore= load_vectorstore(chunks, embeddings)
retriever=vectorstore.as_retriever(search_kwargs={"k":3})
prompt= ChatPromptTemplate.from_messages([
    ("system", """
    Tu es un assistant conversationnel pour les clients de l'entreprise Technova.

Réponds uniquement à partir du contexte fourni.

Si la réponse n'est pas présente dans le contexte, dis clairement que tu ne sais pas et n'utilise pas ta mémoire interne.
"""), 
    MessagesPlaceholder("chat_history"),
    ("human", """
    Contexte :

    {context}

    Question :

    {input}
    """ ) ])
llm= load_llm()
document_chain= create_stuff_documents_chain(llm, prompt)
rag_chain= create_retrieval_chain(retriever, document_chain)

# ====================================== #
# configuration de l'interface chatbot
# ====================================== #
if prompt:= st.chat_input("Poser une question"):
    with st.chat_message("user"):
         st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content": prompt})
    
    #conversion de la mémoire conversationnelle
    def conversion(streamlit_history):
        llm_history=[]
        for msg in streamlit_history:
            if msg["role"] == "user":
               llm_history.append(HumanMessage(content= msg["content"]))
            else:
               llm_history.append(AIMessage(content= msg["content"]))
        return llm_history
    history= conversion(st.session_state.messages)
            
    def stream_response():
        for chunk in rag_chain.stream({"input": prompt, "chat_history":history}):
            if "answer" in chunk:
                yield chunk['answer']
    
    with st.chat_message("assistant"):
        response= st.write_stream(stream_response())
    st.session_state.messages.append({"role":"assistant", "content":response})

# ===================================== #
#               sidebar
# ===================================== #
with st.sidebar:
    st.title("Paramètres")
    if st.button("Effacer l'historique"):
        st.session_state.messages=[]
