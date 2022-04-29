function json_import() {
  var xhr = new XMLHttpRequest()
  xhr.open('GET', '/data', true)
  xhr.responseType = 'json'
  xhr.onload = function () {
    var status = xhr.status
    if (status === 200) {
      createTableRow(xhr.response)
    } else {
      console.log(status, xhr.response)
    }
  }
  xhr.send()
}

function createTableRow(hn_data) {
  for (var i = 0; i < hn_data.length; i++) {
    obj = hn_data[i]
    var newTableRow = document.createElement('tr')

    var pointsColumn = document.createElement('td')
    pointsColumn.appendChild(document.createTextNode(obj.points.toString()))
    newTableRow.appendChild(pointsColumn)

    var titleColumn = document.createElement('td')
    titleColumn.appendChild(document.createTextNode(obj.title))
    newTableRow.appendChild(titleColumn)

    var linkColumn = document.createElement('td')
    var link = document.createElement('a')
    link.appendChild(document.createTextNode(obj.link))
    link.href = obj.link
    linkColumn.appendChild(link)
    newTableRow.appendChild(linkColumn)

    var table = document.getElementById('hacker-news-table')
    table.insertAdjacentElement('beforeend', newTableRow)
  }
}

json_import()
