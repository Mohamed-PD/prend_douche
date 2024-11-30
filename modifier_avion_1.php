<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modifier un Avion</title>
    
</head>
<style>
        body {
            font-family: Arial, sans-serif;
        }

        form {
            max-width: 400px;
            margin: 0 auto;
        }

        label, input {
            display: block;
            margin-bottom: 10px;
        }
    </style>
<body>

    <center><h2>Modifier un Avion</h2></center>

    <center>
        
        <form action="modifier_avion_2.php" method="post">
        <label >Sélectionnez l'avion à Modifier :</label>
        <select name="id_avion" required>
          
            <?php
            
            $server='localhost';
            $utilisateur='root';
            $motpasse='';
            $base='gestion des v';

            $connection=mysqli_connect($server,$utilisateur,$motpasse,$base);

            
            $sql = "SELECT id_avion FROM avion";
            $result = mysqli_query($connection,$sql);

           
            while ($row = mysqli_fetch_row($result)) {
                echo "<option>" . $row[0] . "</option>";
            }

        
            ?>
        </select>
        <style>

.btnn:hover{
    background: #fff;
    color: #ff0000;
}


.btnn a{
    text-decoration: none;
    color: #000;
    font-weight: bold;
}
 </style>

        <button type="submit" class="btnn">Modifier avion</button>
        <button type="submit" class="btnn"> <a href="Interface.html">Revenir</button></a>
    </form>

    </center>
    
</body>
</html>
