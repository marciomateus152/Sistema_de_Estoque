# 📦 ESTOQUE PRO | Sistema de Gestão Full-Stack

Este é um sistema de controle de inventário robusto, desenvolvido para gerenciar produtos, categorias e métricas financeiras em tempo real. O projeto une o poder do processamento back-end em Python com uma interface moderna, intuitiva e totalmente responsiva.

---

## 🛠️ Tecnologias e Ferramentas

| Categoria | Tecnologia |
| :--- | :--- |
| **Linguagem Principal** | Python 3.x |
| **Framework Web** | Flask |
| **Banco de Dados** | MySQL (XAMPP / phpMyAdmin) |
| **Interface (UI)** | HTML5 & Tailwind CSS |
| **Segurança** | Werkzeug (Hash de senhas) & Flask Sessions |
| **Manipulação de Dados** | Bibliotecas CSV e IO |
| **Versionamento** | Git & GitHub |

---

## 📊 Fluxograma do Sistema

O fluxo abaixo representa a arquitetura de comunicação entre o usuário, o servidor Flask e a persistência de dados:

```mermaid
graph TD
    A[Início: Página de Login] --> B{Autenticação}
    B -- Falha --> A
    B -- Sucesso --> C[Painel Geral / Dashboard]
    
    C --> D[Cálculo de Métricas]
    D --> D1[Total de Itens]
    D --> D2[Valor de Investimento]
    D --> D3[Lucro Projetado]
    D --> D4[Alertas de Estoque Mínimo]
    
    C --> E[Operações CRUD]
    E --> E1[Registrar Novo Produto]
    E --> E2[Excluir Produto Existente]
    E --> E3[Editar Informações de Itens]
