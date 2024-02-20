from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
import json
import secrets

db = SQLAlchemy()

class DimTipoCampanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    def __init__(self, nome):
        self.nome = nome
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    permissions = db.Column(db.JSON, nullable=True)

    def __init__(self, username, email, password, permissions=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.permissions = permissions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_permission(self, permission):
        if self.permissions is None:
            self.permissions = []
        self.permissions.append(permission)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'permissions': self.permissions
        }
"""
generate_password_hash e check_password_hash são funções do Werkzeug para gerar e verificar hashes de senha de forma segura.

permissions é armazenado como uma string, mas se você desejar armazenar uma lista, pode considerar transformá-la em um formato como JSON ou usar uma tabela de relacionamento se houver uma relação de muitos para muitos entre usuários e permissões.

O método set_password é usado para definir a senha do usuário e automaticamente gerar o hash.

check_password é usado para verificar se a senha fornecida corresponde ao hash armazenado.

A função add_permission é um exemplo de como você pode adicionar permissões à lista. Certifique-se de tratar casos em que permissions é None inicialmente.

A função to_dict é um exemplo de como você pode converter o objeto User em um dicionário, o que pode ser útil ao serializar o objeto para JSON em suas respostas de API, por exemplo. Você pode personalizá-la conforme necessário.
"""

class Campanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    criador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    dt_criacao = db.Column(db.DateTime, nullable=False)
    dt_inicio = db.Column(db.Date, nullable=False)
    dt_fim = db.Column(db.Date, nullable=False)
    meta = db.Column(db.Float, nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey(DimTipoCampanha.__tablename__ + '.id'), nullable=False)
    
    criador = db.relationship('User', backref='campanhas', foreign_keys=[criador_id])
    tipo = db.relationship('DimTipoCampanha', backref='campanhas', foreign_keys=[tipo_id])

    def __init__(self, nome, criador_id, dt_inicio, dt_fim, meta, tipo_id):
        # Obtenha o fuso horário da America/Recife
        tz_recife = pytz.timezone('America/Recife')
        
        self.nome = nome
        self.criador_id = criador_id
        self.dt_criacao = datetime.now(tz_recife)
        self.dt_inicio = dt_inicio
        self.dt_fim = dt_fim
        self.meta = meta
        self.tipo_id = tipo_id
        
        
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'criador': self.criador.username if self.criador else None,
            'criador_id': self.criador.id if self.criador else None,
            'dt_criacao': self.dt_criacao,
            'dt_inicio': self.dt_inicio.isoformat(),
            'dt_fim': self.dt_fim.isoformat(),
            'meta': self.meta,
            'tipo': self.tipo.nome
        }
"""
id é a chave primária da campanha.
nome é o nome da campanha.
dt_inicio e dt_fim são campos de data que representam a data de início e término da campanha, respectivamente.
meta é o valor em Reais (R$) que a campanha pretende alcançar.
tipo é o tipo de campanha, como "rifa", "doação espontânea" e assim por diante.
A função to_dict é um método opcional que converte um objeto Campanha em um dicionário, o que pode ser útil ao serializar o objeto para JSON em suas respostas de API
"""

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    cidade = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(50), default='Pernambuco', nullable=False)
    pais = db.Column(db.String(50), default='Brasil', nullable=False)

    def __init__(self, nome, telefone=None, cidade=None, estado='Pernambuco', pais='Brasil'):
        self.nome = nome
        self.telefone = telefone
        self.cidade = cidade
        self.estado = estado
        self.pais = pais

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'cidade': self.cidade,
            'estado': self.estado,
            'pais': self.pais
        }
"""
id é a chave primária da tabela Pessoa.
nome é o nome da pessoa.
telefone é o número de telefone da pessoa (pode ser nulo).
cidade, estado, e pais são informações de localização.
Os campos estado e pais têm valores padrão configurados como "Pernambuco" e "Brasil", respectivamente. Esses valores padrão serão utilizados se não for fornecido um valor durante a criação de uma nova instância da classe Pessoa.

A função to_dict é novamente um método opcional que converte um objeto Pessoa em um dicionário, o que pode ser útil ao serializar o objeto para JSON em suas respostas de API.
"""

class Rifa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_campanha = db.Column(db.Integer, db.ForeignKey('campanha.id'), nullable=False)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    disponibilidade = db.Column(db.String(15), nullable=False, default='Disponivel')
    dt_compra = db.Column(db.DateTime, nullable=True)
    vendedor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    num_sorteado = db.Column(db.String(3), nullable=False, default='Não')

    def __init__(self, id_campanha, id_pessoa, numero):
        self.id_campanha = id_campanha
        self.id_pessoa = id_pessoa
        self.numero = numero

    def comprar_rifa(self, id_pessoa, vendedor=None):
        self.id_pessoa = id_pessoa
        self.vendedor = vendedor
        self.disponibilidade = 'Comprada'
        
        # Obtenha o fuso horário da America/Recife
        tz_recife = pytz.timezone('America/Recife')
        
        # Aplique o fuso horário à data e hora atual
        self.dt_compra = datetime.now(tz_recife)

    def sortear_rifa(self):
        self.num_sorteado = 'Sim'

    def to_dict(self):
        return {
            'id': self.id,
            'id_campanha': self.id_campanha,
            'id_pessoa': self.id_pessoa,
            'numero': self.numero,
            'disponibilidade': self.disponibilidade,
            'dt_compra': self.dt_compra.isoformat() if self.dt_compra else None,
            'vendedor': self.vendedor,
            'num_sorteado': self.num_sorteado
        }
"""
id é a chave primária da tabela Rifa.
id_campanha e id_pessoa são chaves estrangeiras que se referem às tabelas Campanha e Pessoa, respectivamente.
numero é o número da rifa.
disponibilidade é um campo que indica se a rifa está disponível para compra ou já foi comprada.
dt_compra armazena a data e hora em que a rifa foi comprada.
vendedor é uma chave estrangeira que se refere à tabela Usuario, representando o vendedor da rifa.
num_sorteado indica se o número foi sorteado ou não.
Os métodos comprar_rifa e sortear_rifa são exemplos de como você pode alterar o estado da rifa durante a compra e o sorteio. A função to_dict é, mais uma vez, um método opcional que converte um objeto Rifa em um dicionário.
"""

class Sorteio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_campanha = db.Column(db.Integer, db.ForeignKey('campanha.id'), nullable=False)
    dt_sorteio = db.Column(db.DateTime, nullable=False)
    id_rifa = db.Column(db.Integer, db.ForeignKey('rifa.id'), nullable=False)
    num_sorteado = db.Column(db.Integer, nullable=False)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    validacao = db.Column(db.String(32), nullable=False)

    def __init__(self, id_campanha, id_rifa, num_sorteado, id_pessoa):
        self.id_campanha = id_campanha
        self.dt_sorteio = datetime.utcnow()
        self.id_rifa = id_rifa
        self.num_sorteado = num_sorteado
        self.id_pessoa = id_pessoa
        self.validacao = self._gerar_codigo_validador()

    def _gerar_codigo_validador(self):
        # Método simples para gerar um código validador usando secrets.token_hex
        return secrets.token_hex(16)

    def to_dict(self):
        return {
            'id': self.id,
            'id_campanha': self.id_campanha,
            'dt_sorteio': self.dt_sorteio.isoformat(),
            'id_rifa': self.id_rifa,
            'num_sorteado': self.num_sorteado,
            'id_pessoa': self.id_pessoa,
            'validacao': self.validacao
        }
"""
id é a chave primária da tabela Sorteio.
id_campanha é uma chave estrangeira que se refere à tabela Campanha.
dt_sorteio é a data e hora do sorteio.
id_rifa é uma chave estrangeira que se refere à tabela Rifa.
num_sorteado indica se o número da rifa foi sorteado ou não.
id_pessoa é uma chave estrangeira que se refere à tabela Pessoa.
validacao é um código validador gerado para o sorteio.
O método _gerar_codigo_validador é utilizado para gerar um código validador usando a função secrets.token_hex, que gera um token hexadecimal seguro. 
"""

