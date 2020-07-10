// pages/theConcreteRecordPage/theConcreteRecordPage.js
var amapFile = require('../../libs/amap-wx.js');
var config = require('../../libs/config.js');
const app = getApp();
Page({
  data: {
    scrollHeight: 0, //页面高度
    TianAPInewsList: [], //默认数据列表
    scrollTop: 0, //Y轴滚动条位置
    touchXStart: 0, //X轴开始位置
    touchYStart: 0, //Y轴开始位置
    currentPage: 1, //默认页数
  },
  onLoad: function () {
    //this.adduser();
    this.loadNewslList(7);
    wx.showShareMenu({
      withShareTicket: true
    })
  },
  initNewsData: function () { //初始化数据
    this.setData({
      scrollTop: 0,
      TianAPInewsList: [],
      currentPage: 1,
      scrollHeight: 0
    });
  },
  refreshNewList: function (e) { //获取最新数据
    this.initNewsData();
    this.loadNewslList(this.data.currentID);
  },
  loadMoreNews: function (e) { //加载更多新闻数据
    this.setData({ currentPage: this.data.currentPage + 1 });
    this.loadNewslList(this.data.currentID);
  },
  setCurrentYScroll: function (event) { //设置当前Y轴滚动条位置
    this.setData({
      scrollTop: event.detail.scrollTop
    });
  },
  loadNewslList: function (NewsTypeId = "") { //加载新闻列表
    var that = this;
    wx.showLoading({ title: '加载中...' })
    var user = wx.getStorageSync('user');
    console.log(user)
    wx.request({
      url: 'http://127.0.0.1:5000/wxuser_navigation_get/' + user.openid + '/',
      success: function (res) {
        console.log(res)
        let temp_data = res.data.newslist;
        that.setData({ TianAPInewsList: temp_data });

        wx.getSystemInfo({ //设置scroll内容高度
          success: function (res) {
            that.setData({
              scrollHeight: res.windowHeight,
            });
          }
        });
        wx.hideLoading() //关闭加载提示
      }
    })
  },

  handerNavigator: function (e) { //点击新闻列表跳转
    var id = e.currentTarget.dataset.id // 新闻url 
    app.globalData.endLongitude=e.currentTarget.dataset.end_longitude;
    app.globalData.endLatitude=e.currentTarget.dataset.end_latitude;
    app.globalData.endaddress = e.currentTarget.dataset.endaddress;
    app.globalData.startLatitude = e.currentTarget.dataset.start_latitude;
    app.globalData.startLongitude = e.currentTarget.dataset.start_longitude;
    app.globalData.startaddress = e.currentTarget.dataset.startaddress;
    app.globalData.city = e.currentTarget.dataset.city;
    console.log(app.globalData)
    wx.navigateTo({
      url: '/pages/det/det',
    })
    
  }
});