from agents.CoordinatorAgent import CoordinatorAgent

def main():
    # Inicializa o CoordinatorAgent
    coordinator = CoordinatorAgent()


    # Executa o fluxo de trabalho completo
    coordinator.run()

if __name__ == "__main__":
    main()
