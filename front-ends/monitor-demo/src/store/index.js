/*定义了一个Vuex存储，用于管理Vue应用的状态*/
import { createStore } from 'vuex'
import Cookie from 'js-cookie'

export default createStore({
  // 对象包含应用中需要管理的所有状态
  state: {
    isCollapse: true,   // 控制侧边栏的展开或折叠状态
    currentMenu: null,  // 表示当前选中的菜单项
    tabsList: [
      {
        path: '/',
        name: 'home',
        label: '首页',
        icon: 'home',
        url: 'home/HomePage'
      }
    ],                  // 存储打开的标签页信息
    menu: [],           // 存储菜单项的数组
    token: ''           // 用于认证的token字符串
  },
  getters: {
  },
  // 对象包含改变应用状态的方法
  mutations: {
    // 切换isCollapse的值
    updateIsCollapse(state, payload='使用折叠') {
      console.log(payload);
      state.isCollapse = !state.isCollapse
    },

    // 设置当前选中的菜单项，并在tabsList中添加或忽略该菜单项
    selectMenu(state, val) {
      // 判断
      // val.name == 'home' ? (state.currentMenu = null) : (state.currentMenu = val)

      if (val.name == 'home') {
        state.currentMenu = null
      } else {
        state.currentMenu = val
        let result = state.tabsList.findIndex(item => item.name === val.name)
        result == -1 ? state.tabsList.push(val) : ''
      }
    },

    // 关闭一个标签页
    closeTab(state, val) {
      let res = state.tabsList.findIndex(item => item.name === val.name)
      state.tabsList.splice(res, 1)

    },

    // 设置菜单项，并在本地存储中保留这个菜单
    setMenu(state, val) {
      state.menu = val
      localStorage.setItem('menu', JSON.stringify(val))
    },

    // 从本地存储加载菜单项，并使用路由动态添加菜单对应的路由
    addMenu(state, router) {
      if (!localStorage.getItem('menu')) {
        return
      }
      const menu = JSON.parse(localStorage.getItem('menu'))
      console.log(menu)
      state.menu = menu

      const menuArray = []

      menu.forEach(item => {
        if (item.children) {
          item.children = item.children.map(item => {
           
          let url = `../views/${item.url}.vue`
            console.log(url)
            item.component = () => import(url)
            return item
          })
          menuArray.push(...item.children)
        } else {
         
          let url = `../views/${item.url}.vue`
          console.log("else: "+url)
          item.component = () => import(url)
          menuArray.push(item)
        }
      })

      menuArray.forEach(item => {
        router.addRoute('myhome', item)
      })
    },

    // 清除菜单项和本地存储中的菜单数据。
    cleanMenu(state) {
      state.menu = []
      localStorage.removeItem('menu')
    },

    // 设置认证token，并在Cookie中保存
    setToken(state, val) {
      state.token = val
      Cookie.set('token', val)
    },

    // 清除认证token和Cookie中的token
    clearToken(state) {
      state.token = ''
      Cookie.remove('token')
    },

    // 从state或Cookie中获取token
    getToken(state) {
      state.token = state.token || Cookie.get('token')
    },

    clearTabsList(state) {
      state.tabsList = [];  // 清空tabsList数组
    }

  },

  // 定义触发mutations的方法
  actions: {
  },

  // 对象允许将store分割成模块，每个模块拥有自己的state
  modules: {
  }
})
