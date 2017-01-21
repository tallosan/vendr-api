<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="/css/main.css?v=1">
<link href="https://fonts.googleapis.com/css?family=Quicksand:300,400,700" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Raleway:100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Open+Sans:100,200,300,300i,400,400i,600,600i,700,700i,800,800i" rel="stylesheet">

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<title>Kangaa</title>
</head>

<body>
	<div id = "site-wrapper">
		<div id = "home" class = "overlay">
		</div>
		<div class = "top-nav">
			<div class = "logo-container">
				<p>Kangaa</p>
			</div>
			<div class = "top-menu-container">
				<div>
					Link 1
				</div>
				<div>
					Link 2
				</div>
				<div>
					Link 3			
				</div>
				<div>
					Link 4
				</div>
				<div>
					Link 5
				</div>
			</div>
		</div>
		<div id = "search-container">
			<div class = "search-filter current-filter">
				<span>
					Residential
				</span>
			</div>
			<div class = "search-filter last-filter">
				<span>
					Commercial
				</span>
			</div>
			<form action="/search.php" method="get">
				<input type="search" placeholder="Destination, City, Address" name = "search">
				<div class = "buy-rent-container">
					<div class = "selected-filter">
						<span>
						 	Buy
						</span>
					</div>
					<div>
						<span>
						 	Rent
						</span>
					</div>
				</div>
				<div class = "search-button" onclick = "$(this).closest('form').submit();">
					<div>
						<div>
						<img src = "images/search-icon-s-w.png">
						</div>
						<div>
						<span>Search</span>
						</div>
					</div>
				</div>
			</form>
			<div id = "filter-containers">
				<div class = "filter">
					<span>
						Price
					</span>
				</div>
				<div class = "filter">
					<span>
						Type
					</span>
				</div>
				<div class = "filter">
					<span>
						Square Footage
					</span>
				</div>
				<div class = "filter">
					<span>
						Bedrooms
					</span>
				</div>
				<div class = "filter">
					<span>
						Bathrooms
					</span>
				</div>
			</div>
		</div>
	</div>
</body>
</html>