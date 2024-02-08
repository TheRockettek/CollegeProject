<template>
  <div>
    <Disclosure as="nav" class="border-b border-gray-200 bg-white" v-slot="{ open }">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex h-16 justify-between">
          <div class="flex">
            <div class="flex flex-shrink-0 items-center">
              <a href="/">
                <img class="block h-8 w-auto lg:hidden" src="/logo.svg" alt="Home" />
                <img class="hidden h-8 w-auto lg:block" src="/logo.svg" alt="Home" />
              </a>
            </div>
          </div>
          <div v-if="$store.getters.isLoggedIn" class="hidden sm:ml-6 sm:flex sm:items-center">
            <div
              class="relative max-w-xs text-left rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              <div class="text-base leading-none font-medium text-gray-800">
                {{ $store.getters.getCurrentUser?.name }}
              </div>
              <div class="block leading-none text-sm font-medium text-gray-500">
                {{ $store.getters.getCurrentUser?.role }}
              </div>
            </div>
            <div>
              <a href="/logout" class="block text-gray-500 hover:text-gray-900 underline ml-6">
                <span class="mr-2">Logout</span>
                <svg class="icon w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
                  <path
                    d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"
                  />
                </svg>
              </a>
            </div>
          </div>
          <div v-else class="hidden sm:ml-6 sm:flex sm:items-center">
            <div class="relative flex bg-white text-sm focus:outline-none">
              <a href="/login" class="block p-2 text-gray-500 hover:text-gray-900 underline">
                <span class="mr-2">Login</span>
                <svg class="icon w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
                  <path
                    d="M217.9 105.9L340.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L217.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1L32 320c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM352 416l64 0c17.7 0 32-14.3 32-32l0-256c0-17.7-14.3-32-32-32l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64 0c53 0 96 43 96 96l0 256c0 53-43 96-96 96l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32z"
                  />
                </svg>
              </a>
            </div>
          </div>
          <div class="-mr-2 flex items-center sm:hidden">
            <!-- Mobile menu button -->
            <DisclosureButton
              class="relative inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              <span class="absolute -inset-0.5" />
              <span class="sr-only">Open main menu</span>
              <svg
                v-if="!open"
                class="block h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                />
              </svg>
              <svg
                v-else
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </DisclosureButton>
          </div>
        </div>
      </div>

      <DisclosurePanel class="sm:hidden">
        <div class="space-y-1 pb-3 pt-2">
          <DisclosureButton
            v-for="item in navigation"
            :key="item.name"
            as="a"
            :href="item.href"
            :class="[
              item.current
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-transparent text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800',
              'block border-l-4 py-2 pl-3 pr-4 text-base font-medium'
            ]"
            :aria-current="item.current ? 'page' : undefined"
            >{{ item.name }}</DisclosureButton
          >
        </div>
        <div v-if="$store.getters.isLoggedIn" class="border-t border-gray-200 p-4">
          <div>
            <div class="text-base font-medium text-gray-800">
              {{ $store.getters.getCurrentUser.name }}
            </div>
            <div class="block text-sm font-medium text-gray-500">
              {{ $store.getters.getCurrentUser.role }}
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <a href="/logout" class="block text-gray-500 hover:text-gray-900 underline">
              <span class="mr-2">Logout</span>
              <svg class="icon w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
                <path
                  d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"
                />
              </svg>
            </a>
          </div>
        </div>
        <div v-else class="border-t border-gray-200 p-4">
          <a href="/login" class="block p-2 text-gray-500 hover:text-gray-900 underline">
            <span class="mr-2">Login</span>
            <svg class="icon w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
              <path
                d="M217.9 105.9L340.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L217.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1L32 320c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM352 416l64 0c17.7 0 32-14.3 32-32l0-256c0-17.7-14.3-32-32-32l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64 0c53 0 96 43 96 96l0 256c0 53-43 96-96 96l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32z"
              />
            </svg>
          </a>
        </div>
      </DisclosurePanel>
    </Disclosure>

    <ToastView />
  </div>
</template>

<script setup>
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import ToastView from '@/components/ToastView.vue'
</script>
