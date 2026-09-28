#pragma once
#include "identidade.hpp"
#include <map>
#include <set>

struct Medicao {
    double valor;
    std::string unidade;
};

// Fornecido: T varia o item, preservando a chave e o contrato do catálogo.
template<typename T>
class Catalogo {
    std::map<IdSensor, T> itens_;
public:
    bool inserir(const IdSensor& id, const T& item) {
        auto [it, inserido] = itens_.emplace(id, item);
        return inserido;
    }
    const T* buscar(const IdSensor& id) const {
        auto it = itens_.find(id);
        if (it == itens_.end()) return nullptr;
        return &it->second;
    }
    bool remover(const IdSensor& id) {
        return itens_.erase(id) > 0;
    }
    std::size_t quantidade() const { return itens_.size(); }
    std::set<IdSensor> ids() const {
        std::set<IdSensor> resultado;
        for (const auto& entrada : itens_) resultado.insert(entrada.first);
        return resultado;
    }
};