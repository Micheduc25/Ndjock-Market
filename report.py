css='''<style type='text/css'>
    body{ background-image:url("mybg.jpg");background-color:rgba(255,0,0,0.15); text-align:center; margin:0px;}

    #Header{ background-color: rgba(0,12,0,0.7);
    width:400px;
    overflow:hidden;
    width:100%;
    height:20%;
    background-image:url("cafeBg.jpg");
    background-repeat:no-repeat;
    
    }
    #Heading{ width:100%;
            height:100%;
            background-color:rgba(255,0,0,0.4);
            text-shadow:5px 7px 0px rgba(0,0,0,0.2);
            overflow:hidden;
            text-align:center;
}    

    tr:nth-child(even){background-color: rgba(255,0,0,0.5);}
    tr{border:0px;padding:0px;margin:0px;}
    #thebody{width:100%;height:70%;}
    table{margin-left:auto;margin-right:auto; padding-top:10%;border:0px; height:100% ;font-size:17pt;font-family:consolas;}
    td{text-align:left;border:0px;padding:0px;margin:0px;}
    td:nth-child(odd){text-align:right; padding-right:10px;}
    th{background-color: rgba(255,0,0,0.6);}
    </style>'''
reportcode=''' 

<!DOCTYPE HTML>
<html lang='fr'>
<head>
    
    <meta name="keywords" content="rapport , produit,vente,marche">
    
    <link rel="shortcut icon" href="">
    {}

    
    <title>Rapport Ndjock Market</title>
</head>
<body >

<div id="Header">

    <div id="Heading">

        <h1>Rapport du {}</h1>

    </div>
   

</div>

<div id="Upperbody">
<div id="Welcome">

</div>

<div id='thebody'>
<table>
<th colspan="2">Rapport</th>
<tr> <td>Nom du Produit </td> <td>{}</td> </tr>
<tr> <td>Prix d'une Unité </td> <td>{}</td> </tr>
<tr> <td>Stock Initiale </td> <td>{}</td> </tr>
<tr> <td>Reste de la journée Précédente :</td> <td>{}</td> </tr>
<tr> <td>Reste d'aujourd'hui </td> <td>{}</td> </tr>
<tr> <td>Quantité Vendu </td> <td>{}</td> </tr>
<tr> <td>Sommme Vendu </td> <td>{}</td> </tr>

</table>
</div>

</body>
</html>



'''

class Report:
    def __init__(self,date,nom,prix,stock,resthier,reste,qtyvendu,smvendu):
        self.date=date
        self.nom=nom
        self.prix=prix
        self.stock=stock
        self.restehier=resthier
        self.reste=reste
        self.qtyvendu=qtyvendu
        self.smvendu=smvendu

    def generateReport(self):
        code=reportcode.format(css,self.date,self.nom,self.prix,self.stock,self.restehier,self.reste,self.qtyvendu,self.smvendu)
        return code