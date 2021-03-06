import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from controller.DividaCTR import DividaCTR
from controller.ClienteCTR import clienteCTR
from controller.ProdutoCTR import ProdutoCTR

class TelaFiado(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Dividas dos clientes'
        self.left = 300
        self.top = 100
        self.width = 600
        self.height = 630 

        self.nomeDigitado = None
        
        self.initUI()

    def initUI(self):
        
        self.bntBuscarCliente = QPushButton('Buscar cliente ', self)
        self.lbTotal = QLabel(' DÍVIDA TOTAL R$: 00,00 ', self)
        self.lbTotal.setStyleSheet('QLabel {font: bold; font: 20px; background-color: #F22613; border-radius: 5px}')
        self.bntBuscarCliente.setStyleSheet('QPushButton {font: bold; font: 20px;}')
        self.bntBuscarCliente.clicked.connect(self.bntBuscarClienteClicked)

        self.bntQuitar = QPushButton('Quitar Dívida', self)
        self.bntQuitar.setStyleSheet('QPushButton {font: bold; font: 20px;}')
        self.bntQuitar.clicked.connect(self.bntQuitarClicked)

        self.campoBuscaCliente = QLineEdit(self)
        #self.campoBuscaCliente.setGeometry(0,0,200,50)

        self.tabela = self.createTable()

        self.widget = QWidget(self)
        layout = QGridLayout()
        self.widget.setLayout(layout)
        layout.addWidget(self.tabela,3,0,20,15)
        layout.addWidget(self.bntBuscarCliente,0,1) #(linha, coluna)
        layout.addWidget(self.campoBuscaCliente,0,2)
        layout.addWidget(self.lbTotal,2,2)
        layout.addWidget(self.bntQuitar,2,1)
        

        self.setCentralWidget(self.widget)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
    
    def createTable(self):
        self.tableDividas = QTableWidget(self)
        self.tableDividas.setRowCount(30)
        self.tableDividas.setColumnCount(5)
        self.tableDividas.setItem(0,0,QTableWidgetItem('NOME'))
        self.tableDividas.setItem(0,1,QTableWidgetItem('PRODUTO'))
        self.tableDividas.setItem(0,2,QTableWidgetItem('QTDE'))
        self.tableDividas.setItem(0,3,QTableWidgetItem('DATA_COMPRA'))
        self.tableDividas.setItem(0,4,QTableWidgetItem('TOTAL R$'))

        self.tableDividas.setEditTriggers(QTableWidget.NoEditTriggers) #bloqueia todas as celulas

        self.tableDividas.setStyleSheet('QTableWidget {font: 14px; font: bold}')
        
        return self.tableDividas
    
    def limparTabela(self):
        for linha in range(29):
            for coluna in range(5):
                self.tableDividas.setItem(linha,coluna,QTableWidgetItem(' '))


    def bntBuscarClienteClicked(self):
        self.nomeDigitado = self.campoBuscaCliente.text()
        if(self.nomeDigitado == clienteCTR.buscarCliente(self.nomeDigitado)):
            self.clienteLocalizado = True
            aviso = QMessageBox.information(self, '', 'Cliente {}, localizado '.format(self.nomeDigitado))
            self.campoBuscaCliente.setStyleSheet('QLineEdit {background: #2ECC71}')
            self.dividas = DividaCTR.buscarDivida(self.nomeDigitado)
            print(len(self.dividas))
            print(DividaCTR.buscarDivida(self.nomeDigitado))

            for linha in range(len(DividaCTR.buscarDivida(self.nomeDigitado))):
                for coluna in range(5):
                    self.tabela.setItem((linha+1), coluna,QTableWidgetItem('{}'.format(self.dividas[linha][coluna])) )
            print(type(DividaCTR.obterDividaTotal(self.nomeDigitado)))
            
            if(len(self.dividas) != 0):
                self.lbTotal.setText(' DÍVIDA TOTAL R$: {:0.2f}'.format(DividaCTR.obterDividaTotal(self.nomeDigitado)))
            else:
                aviso = QMessageBox.information(self, 'Aviso:', 'Não há dividas a serem quitadas')
        else:
            aviso = QMessageBox.information(self, '', 'Cliente {} NÃO localizado '.format(self.nomeDigitado))
            self.campoBuscaCliente.setStyleSheet('QLineEdit {background: #F22613}')

    def bntQuitarClicked(self):
        avisoExlusão = QMessageBox.question(self, 'Atenção', 'Você deseja realmente quitar a divida do cliente: {}'.format(self.nomeDigitado), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if (avisoExlusão == QMessageBox.Yes):
            DividaCTR.quitarDivida(self.nomeDigitado)
            self.lbTotal.setStyleSheet('QLabel {font: bold; font: 20px; background-color: #00B16A; border-radius: 5px}')
            aviso = QMessageBox.information(self, 'Aviso:', ' A divida do cliente {} foi quitada com sucesso'.format(self.nomeDigitado))
            self.lbTotal.setText(' DÍVIDA TOTAL R$: 00,00')
            self.limparTabela()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    telaFiado = TelaFiado()
    sys.exit(app.exec_())



        