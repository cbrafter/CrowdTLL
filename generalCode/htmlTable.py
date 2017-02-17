def htmlTable(data, filename):
    f = open(filename, 'w')
    header = """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="30">
<style>
#customers {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    font-size: 25px;
    border-collapse: collapse;
    width: 75%;
}

#customers td, #customers th {
    border: 1px solid #ddd;
    padding: 4px;
    text-align: center;
}

#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #c2deed;}

#customers th {
    padding-top: 10px;
    padding-bottom: 10px;
    text-align: center;
    background-color: #005A87;
    color: white;
}

#parent {
  display: flex;
}
#narrow {
  width: 50%;
  margin-left: 3%;
}
#wide {
  flex: 1;
  margin-right: 3%;
}

</style>
</head>
<body>
<div id="parent">
  <div id="wide">
  <table id="customers" align="right">
    <caption>Traffic Light Control Leaderboard</caption>
    <tr>
      <th>Initials</th>
      <th>Time</th>
    </tr>
  """
    for i in range(len(data)):
        header += """<tr>
    <td>{}</td>
    <td>{}</td>
  </tr>
  """.format(data.loc[i][0], data.loc[i][1])
    header += """  <div align="right">
    <iframe width="75%" height="350" src="https://www.youtube.com/embed/Tamzt3m7BaI?autoplay=1&t=13s&loop=1" frameborder="0" allowfullscreen></iframe>
  </div>
</div>

<div id="narrow" align="left">
  <a class="twitter-timeline" data-width="680" data-height="800" data-theme="light" href="https://twitter.com/sotonTraffJam">Tweets by cbrafter</a> 
  <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>

</div>
</body>
</html>
"""
    f.write(header)
    f.close()
