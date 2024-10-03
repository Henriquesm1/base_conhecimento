from . import db

class Conhecimento(db.Model):
    __tablename__ = 'conhecimento'

    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100))
    palavras_chave = db.Column(db.Text)
    exemplo = db.Column(db.Text)  # Novo campo para exemplo opcional
    data_criacao = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Indexes
    __table_args__ = (
        db.Index('idx_pergunta', 'pergunta'),
        db.Index('idx_categoria', 'categoria'),
        db.Index('idx_palavras_chave', 'palavras_chave'),
    )
