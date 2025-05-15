<h1 align="center">🧠 JSOM AI Chatbot</h1>
<h3 align="center">🔍 RAG-based GenAI Assistant for the Jindal School of Management, UT Dallas</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Built%20with%20LangChain%20%26%20Streamlit-0aa15f?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Ollama-Mistral_7B-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

<hr>

<p align="center">
  <img src="assets/demo.gif" alt="JSOM AI Chatbot Demo" width="80%" />
</p>

<hr>

<h2>📌 Overview</h2>

<p>
An intelligent chatbot built using <strong>Retrieval-Augmented Generation (RAG)</strong> to answer queries from over <strong>1,500+ webpages</strong> across the Jindal School of Management (UT Dallas). <br><br>
Deployed with <strong>Streamlit</strong>, powered by <strong>LangChain</strong> + <strong>ChromaDB</strong> + <strong>Mistral via Ollama</strong>.
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>✅ Full pipeline: scrape → clean → chunk → embed → retrieve</li>
  <li>✅ Answer generation using LangChain + Mistral</li>
  <li>✅ Vector database via ChromaDB</li>
  <li>✅ Streamlit interface with ~20–60s latency</li>
  <li>✅ Source-linked answers for transparency</li>
</ul>

<hr>

<h2>🧰 Tech Stack</h2>

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Tools Used</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Web Scraping</td>
      <td><code>Playwright (Python)</code></td>
    </tr>
    <tr>
      <td>Embedding & RAG</td>
      <td><code>LangChain</code>, <code>ChromaDB</code>, <code>Mistral via Ollama</code></td>
    </tr>
    <tr>
      <td>UI / Deployment</td>
      <td><code>Streamlit</code></td>
    </tr>
    <tr>
      <td>Storage & Parsing</td>
      <td><code>JSON</code>, <code>Excel</code>, <code>Pandas</code></td>
    </tr>
  </tbody>
</table>

<hr>

<h2>📁 Project Structure</h2>

<pre>
adaran/
├── app.py
├── qa_chain_mistral.py
├── load_retriever.py
├── embed_pages.py
├── chunk_pages.py
├── tagging_pages.py
├── scraper_playwright.py
├── all_jsom_urls_combined.xlsx
├── cleaned_pages.json, chunked_pages.json, etc.
├── chroma_db/
├── assets/
│   └── demo.gif
└── README.md
</pre>

<hr>

<h2>⚙️ How to Run Locally</h2>

<pre>
# 1. Clone the repo
git clone https://github.com/prathameshnagraj/adaran.git
cd jsom-ai-chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Mistral (via Ollama)
ollama run mistral

# 4. Launch the app
streamlit run app.py
</pre>

<hr>

<h2>🙋‍♂️ Author</h2>

<p>
<strong>Prathamesh Nagraj</strong><br>
<a href="mailto:ppnagraj.work@gmail.com">📧 Email</a> | 
<a href="https://www.linkedin.com/in/prathamesh-nagraj/">🔗 LinkedIn</a>
</p>

<hr>

<p align="center"><em>“Turning information overload into conversational clarity.”</em></p>
