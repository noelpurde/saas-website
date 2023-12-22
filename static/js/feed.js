document.addEventListener('DOMContentLoaded', function () {
    var yourBackchannel = document.querySelector('.your-backchannel');
    var you = document.querySelector('.you');
    var yourBackchannelFeedActivity = document.querySelector('.your-backchannel-feed-activity');
    var youFeedActivity = document.querySelector('.you-feed-activity');

    // Set default styles
    yourBackchannel.style.fontWeight = 'bold';
    youFeedActivity.style.display = 'none';

    yourBackchannel.onclick = function () {
        toggleDiv('your-backchannel', 'you', yourBackchannelFeedActivity, youFeedActivity);
    };

    you.onclick = function () {
        toggleDiv('you', 'your-backchannel', youFeedActivity, yourBackchannelFeedActivity);
    };
});

function toggleDiv(selectedDiv, otherDiv, selectedContent, otherContent) {
    var selected = document.querySelector('.' + selectedDiv);
    var other = document.querySelector('.' + otherDiv);

    if (selected.style.fontWeight !== 'bold') {
        selected.style.fontWeight = 'bold';
        other.style.fontWeight = 'normal';

        selectedContent.style.display = 'flex';
        selectedContent.style.flexDirection = 'column';
        selectedContent.style.flex = '1';
        selectedContent.style.order = '2';
        otherContent.style.display = 'none';
    }
}
