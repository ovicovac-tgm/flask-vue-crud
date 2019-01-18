import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Todos from '@/components/Todos';
import Order from '@/components/Order';
import OrderComplete from '@/components/OrderComplete';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Todo',
      component: Todos,
    }
  ],
  mode: 'hash',
});
