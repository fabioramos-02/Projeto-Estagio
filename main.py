from agents.CoordinatorAgent import CoordinatorAgent

def main():
    # Inicializa o CoordinatorAgent
    coordinator = CoordinatorAgent()

    # Executa o fluxo de trabalho completo para todas as URLs do banco de dados
    coordinator.run()

if __name__ == "__main__":
    main()
