function json_import() {
  let jsonData
  fetch('./hacker-news.json')
    .then((response) => response.json())
    .then((json) => (jsonData = json))

  for (id in json) {
    createTableRow(json[points], json[title], json[link])
  }
}

function createTableRow(points, title, link) {
  var newTableRow = document.createElement('tr')

  var pointsColumn = document.createElement('td')
  pointsColumn.innerHTML(points)
  newTableRow.appendChild(pointsColumn)

  var titleColumn = document.createElement('td')
  titleColumn.innerHTML(title)
  newTableRow.appendChild(titleColumn)

  var linkColumn = document.createElement('td')
  linkColumn.innerHTML(link)
  newTableRow.appendChild(linkColumn)

  var table = document.getElementById('hacker-news-table')
  table.insertAdjacentElement('beforeend', newTableRow)
}

json_import()
