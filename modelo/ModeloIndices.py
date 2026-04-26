import math

class ModeloIndices:
    def __init__(self):
        self.res_tabla = []
        self.cant_estructuras = 0

    def calcular_indices(self, tipo, niveles, tam_bloque, cant_reg, tam_reg, tam_reg_ind):
        self.res_tabla = []
        
        # 1. Cálculos de la Estructura Principal
        reg_x_bloque = tam_bloque // tam_reg
        cant_bloq_regis = math.ceil(cant_reg / reg_x_bloque)
        
        self.res_tabla.append(["1", "Cant. registros", str(cant_reg)])
        self.res_tabla.append(["1", "Reg. x Bloque", str(reg_x_bloque)])
        self.res_tabla.append(["1", "Bloques", str(cant_bloq_regis)])

        # 2. Cálculos del Índice (Nivel 1)
        ind_x_bloque = tam_bloque // tam_reg_ind
        
        if tipo == "Primario":
            cant_indices = cant_bloq_regis
        else: # Secundario
            cant_indices = cant_reg

        cant_bloq_indic = math.ceil(cant_indices / ind_x_bloque)

        self.res_tabla.append(["2", "Cant. registros Indice", str(cant_indices)])
        self.res_tabla.append(["2", "Ind x Bloque", str(ind_x_bloque)])
        self.res_tabla.append(["2", "Cant. Bloques Indice", str(cant_bloq_indic)])

        # 3. Multinivel
        nivel_actual = 2
        if niveles == "Multinivel":
            while cant_bloq_indic > 1:
                nivel_actual += 1
                cant_indices_nuevo_nivel = cant_bloq_indic
                cant_bloq_indic = math.ceil(cant_indices_nuevo_nivel / ind_x_bloque)
                
                self.res_tabla.append([str(nivel_actual), "Cant. registros Indice", str(cant_indices_nuevo_nivel)])
                self.res_tabla.append([str(nivel_actual), "Ind x Bloque", str(ind_x_bloque)])
                self.res_tabla.append([str(nivel_actual), "Cant. Bloques Indice", str(cant_bloq_indic)])

        self.cant_estructuras = nivel_actual
        return self.res_tabla, self.cant_estructuras