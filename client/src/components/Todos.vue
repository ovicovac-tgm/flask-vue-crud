<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>TODO</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.todo-modal>Add todo</button>
        <br><br>

        <!-- TODO table -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">todo</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th scope="col">Purchase Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(todo, index) in TODO" :key="index">
              <td>{{ todo.todo }}</td>
              <td>{{ todo.author }}</td>
              <td>
                <span v-if="todo.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>${{ todo.price }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.todo-update-modal
                        @click="edittodo(todo)">
                    Update
                </button>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeletetodo(todo)">
                    Delete
                </button>
                <router-link :to="`/order/${todo.id}`"
                             class="btn btn-primary btn-sm">
                    Purchase
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>

    <!-- add todo modal -->
    <b-modal ref="addtodoModal"
             id="todo-modal"
            todo="Add a new todo"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-todo-group"
                      label="todo:"
                      label-for="form-todo-input">
            <b-form-input id="form-todo-input"
                          type="text"
                          v-model="addtodoForm.todo"
                          required
                          placeholder="Enter todo">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="addtodoForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-group"
                      label="Purchase price:"
                      label-for="form-price-input">
          <b-form-input id="form-price-input"
                        type="number"
                        v-model="addtodoForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-group">
            <b-form-checkbox-group v-model="addtodoForm.read" id="form-checks">
              <b-form-checkbox value="true">Read?</b-form-checkbox>
            </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="edittodoModal"
             id="todo-update-modal"
             todo="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-todo-edit-group"
                      label="todo:"
                      label-for="form-todo-edit-input">
          <b-form-input id="form-todo-edit-input"
                        type="text"
                        v-model="editForm.todo"
                        required
                        placeholder="Enter todo">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-edit-group"
                      label="Purchase price:"
                      label-for="form-price-edit-input">
          <b-form-input id="form-price-edit-input"
                        type="number"
                        v-model="editForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      TODO: [],
      addtodoForm: {
        todo: '',
        author: '',
        read: [],
        price: '',
      },
      editForm: {
        id: '',
        todo: '',
        author: '',
        read: [],
        price: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getTODO() {
      const path = 'http://localhost:5000/TODO';
      axios.get(path)
        .then((res) => {
          this.TODO = res.data.TODO;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addtodo(payload) {
      const path = 'http://localhost:5000/TODO';
      axios.post(path, payload)
        .then(() => {
          this.getTODO();
          this.message = 'todo added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTODO();
        });
    },
    updatetodo(payload, todoID) {
      const path = `http://localhost:5000/TODO/${todoID}`;
      axios.put(path, payload)
        .then(() => {
          this.getTODO();
          this.message = 'todo updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTODO();
        });
    },
    removetodo(todoID) {
      const path = `http://localhost:5000/TODO/${todoID}`;
      axios.delete(path)
        .then(() => {
          this.getTODO();
          this.message = 'todo removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTODO();
        });
    },
    initForm() {
      this.addtodoForm.todo = '';
      this.addtodoForm.author = '';
      this.addtodoForm.read = [];
      this.addtodoForm.price = '';
      this.editForm.id = '';
      this.editForm.todo = '';
      this.editForm.author = '';
      this.editForm.read = [];
      this.editForm.id = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addtodoModal.hide();
      let read = false;
      if (this.addtodoForm.read[0]) read = true;
      const payload = {
        todo: this.addtodoForm.todo,
        author: this.addtodoForm.author,
        read, // property shorthand
        price: this.addtodoForm.price,
      };
      this.addtodo(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.edittodoModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        todo: this.editForm.todo,
        author: this.editForm.author,
        read, // property shorthand
        price: this.editForm.price,
      };
      this.updatetodo(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addtodoModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.edittodoModal.hide();
      this.initForm();
      this.getTODO(); // why?
    },
    onDeletetodo(todo) {
      this.removetodo(todo.id);
    },
    edittodo(todo) {
      this.editForm = todo;
    },
  },
  created() {
    this.getTODO();
  },
};
</script>
