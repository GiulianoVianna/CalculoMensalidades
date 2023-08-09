import sys
import locale
from PyQt5 import QtWidgets, QtGui, uic


class ParcelasApp(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        # Carrega interface
        uic.loadUi('calculo.ui', self)
        self.setFixedSize(300, 710)
        self.table_parcelas.setColumnWidth(0, 230)

        # Configurar o cabeçalho com stylesheet
        header_style = "QHeaderView::section { font-size: 10pt; }"
        self.table_parcelas.horizontalHeader().setStyleSheet(header_style)

        # Configurar a fonte dos itens da tabela
        font = QtGui.QFont("Arial", 12)
        self.table_parcelas.setFont(font)

        # Configurações iniciais
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

        # Conecta eventos
        self.bt_salvar.clicked.connect(self.calcular)

    def obter_dados(self):
        try:
            valor = self.tratar_valor(self.txt_valor.text())
            parcelas = int(self.txt_parcelas.text())
            juros = self.tratar_valor(self.txt_juros.text()) / 100

            # Validar entradas
            if valor <= 0 or parcelas <= 0 or juros < 0:
                raise ValueError("Valores inválidos")

            return valor, parcelas, juros
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))
            return None, None, None

    def tratar_valor(self, valor):
        try:
            return float(valor.replace(',', '.'))
        except ValueError:
            raise ValueError("Por favor, insira um número válido")

    def calcular(self):
        valor, parcelas, juros = self.obter_dados()

        if valor and parcelas and juros:
            montante = valor * (1 + juros)
            vp = montante / parcelas

            self.preencher_tabela(parcelas, vp)
            self.exibir_total(parcelas, vp)

    def preencher_tabela(self, num_parcelas, valor_parcela):
        self.table_parcelas.setRowCount(num_parcelas)

        for i in range(num_parcelas):
            valor_formatado = locale.format_string('%.2f', valor_parcela)
            item = QtWidgets.QTableWidgetItem(valor_formatado)
            self.table_parcelas.setItem(i, 0, item)

    def exibir_total(self, num_parcelas, valor_parcela):
        total = num_parcelas * valor_parcela
        total_formatado = locale.format_string('%.2f', total)
        self.txt_total.setText(total_formatado)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = ParcelasApp()
    window.show()
    sys.exit(app.exec_())
