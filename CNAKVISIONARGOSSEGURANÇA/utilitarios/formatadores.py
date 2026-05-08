import datetime

class Utils:
    @staticmethod
    def formatar_cpf(numero):
        """Formata string de CPF para o padrão 000.000.000-00."""
        texto = "".join(filter(str.isdigit, str(numero))).zfill(11)
        return f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
    
    @staticmethod
    def gerar_foto_ficticia(seed):
        return f"https://picsum.photos/seed/{seed}/320/320"
    
    @staticmethod
    def gerar_usuario_ficticio(seed, colunas):
        # Geramos os dados aqui sem importar o database.py
        from datetime import datetime
        nomes = ["Mariana Silva", "Tiago Almeida", "Beatriz Costa", "Lucas Pereira"]
        nome = nomes[seed % len(nomes)]
        
        return dict(zip(colunas, [
            nome, 
            Utils.formatar_cpf(seed * 3 + 17), 
            f"{nome.lower().replace(' ', '.')}@cnak.com",
            f"(61) 9{seed%10}555-4444",
            "Operacional", "Não Informado", "Brasília-DF", "Sistema",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            Utils.gerar_foto_ficticia(seed)
        ]))