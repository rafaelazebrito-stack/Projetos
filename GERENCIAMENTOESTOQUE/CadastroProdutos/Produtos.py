from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from Locais import LocalEstoqueManager

DB_FILE = Path(__file__).resolve().parent / 'dados_produtos.json'


@dataclass
class Categoria:
    nome: str
    descricao: str = ''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Categoria':
        return cls(**data)


@dataclass
class Produto:
    codigo: str
    nome: str
    descricao: str
    peso: float
    codigobarra: str
    embalagem: str
    composicao_embalagem: str
    data_validade: str
    dimensoes: str
    categoria: str
    dun: str
    ean: str
    quantidade: int = 0
    local_id: Optional[str] = None
    preco_unitario: float = 0.0
    ativo: bool = True
    imagem: Optional[str] = None  # ✅ caminho da imagem

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Produto':
        return cls(**data)


class EstoqueManager:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = Path(db_path) if db_path else DB_FILE
        self.locais = LocalEstoqueManager()
        self._load()

    def _load(self) -> None:
        if not self.db_path.exists():
            self._data = {'produtos': [], 'categorias': [], 'locais': []}
            self._save()
        else:
            self._data = json.loads(self.db_path.read_text(encoding='utf-8'))

        self._data.setdefault('produtos', [])
        self._data.setdefault('categorias', [])
        self._data.setdefault('locais', [])

        self.locais._load_from_data(self._data)

    def _save(self) -> None:
        self._data['locais'] = self.locais.listar_locais_dicts()
        self.db_path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def criar_produto(self, produto: Produto) -> None:
        if self.consultar_produto(produto.codigo):
            raise ValueError("Produto já existe")
        self._data['produtos'].append(produto.to_dict())
        self._save()

    def listar_produtos(self) -> List[Produto]:
        return [Produto.from_dict(p) for p in self._data['produtos']]