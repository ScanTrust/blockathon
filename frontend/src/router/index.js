import Vue from 'vue'
import Router from 'vue-router'
import Ga from 'vue-ga'

import Allergens from '@/components/Allergens'
import Config from '@/config.js'
import ContentWrapper from '@/components/ContentWrapper'
import Ingredients from '@/components/Ingredients'
import More from '@/components/More'
import Nutrition from '@/components/Nutrition'
import Scm from '@/components/ScmData'
import Sustainability from '@/components/Sustainability'
import ConsumerImpact from '@/components/ConsumerImpact'
import EUIPO from '@/components/EUIPO'
// import BlockChain from '@/components/BlockChain'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/?:uid&:qr&:api_key',
      name: 'ContentWrapper',
      component: ContentWrapper,
      props: true,
      children: [
        {
          path: '/nutrition',
          name: 'nutrition',
          component: Nutrition,
          props: true
        }, {
          path: '/ingredients',
          name: 'ingredients',
          component: Ingredients,
          props: true
        }, {
          path: '/allergens',
          name: 'allergens',
          component: Allergens,
          props: true
        }, {
          path: '/sustainability',
          name: 'sustainability',
          component: Sustainability,
          props: true
        }, {
          path: '/more',
          name: 'more',
          component: More,
          props: true
        }, {
          path: '/scm',
          name: 'scm',
          component: Scm,
          props: true
        }, {
          path: '/EUIPO',
          name: 'EUIPO',
          component: EUIPO,
          props: true
        }, {
          path: '/consumer-impact',
          name: 'consumer-impact',
          component: ConsumerImpact,
          props: true
        }
      ]
    }
  ]
})

if (Config.st_config.GA_KEY) {
  Ga(router, Config.st_config.GA_KEY)
}

export default router
