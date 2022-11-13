// var T_BODY = document.getElementById('table').lastChild
// var userX = T_BODY.lastChild
// var userY = T_BODY.children

table = $("#table")
UserInputs = $("#UserInputs")
UserX = $("#UserX")
UserY = $("#UserY")
AddBtn = $("#AddBtn")
hiddenNum = $("#hidden_numbers")

$(AddBtn).on("click", function() {
    n = $("#table tr").length;
    tr_to_append = $(`<tr><td>(${n-1})</td><td>${UserX.val()}</td><td>${UserY.val()}</td><td><input value="edit" class="edit" type="button"></td></tr>`)
    tr_to_append.insertBefore(UserInputs);
    writeToHiddenNum()
        // console.log(n)
        // console.log($('table tr').children(':nth-child(2)').text())
});



$("table").on("click", "input[value='edit']", function(event) {
    target = $(event.target);
    // target.parent().parent().remove();
    target.val('save')
    X = target.parent().parent().children(':nth-child(2)')
    Y = target.parent().parent().children(':nth-child(3)')
    X.empty()
    Y.empty()
    X.append(`<input class="correctX inptNum" type="number">`)
    Y.append(`<input class="correctY inptNum" type="number">`)
    return false;
});



$("table").on("click", "input[value='save']", function(event) {
    target = $(event.target);
    // target.parent().parent().remove();
    target.val('edit')
    nw_X = target.parent().parent().children(':nth-child(2)').children().val()
    nw_Y = target.parent().parent().children(':nth-child(3)').children().val()
    X.empty().append(nw_X)
    Y.empty().append(nw_Y)
    if (nw_X == '' || nw_Y == '') {
        target.parent().parent().remove();
    }
    countIndex()
    writeToHiddenNum()
    return false;
});



function findrows(i) {
    nums = ''
    $(`table tbody tr :nth-child(${i})`).each(function(index, tr) {

        text = $(this).text()
        if ($.isNumeric(text) !== true) {
            return true;
        }
        // console.log(index, tr, text, typeof parseFloat(text));
        // console.log(index, tr, text);
        nums = nums.concat(" ", text);


    });
    return nums
}



function writeToHiddenNum() {
    values = '';
    values = values.concat(`${findrows(2)}`)
    values = values.concat(`,`)
    values = values.concat(`${findrows(3)}`)
    console.log(values)
    hiddenNum.val(values)
}

function countIndex() {
    $('table tbody tr :nth-child(1):contains(()').each(function(index, tr) {
        index += 1
        console.log(tr)
        $(this).text(`(${index})`)
    });
}