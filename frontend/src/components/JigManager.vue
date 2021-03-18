<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col cols="8">
          <h3>Jig Status</h3>
        </b-col>
        <b-col>
          <b-button pill variant="success">Add Jig</b-button>
        </b-col>
      </b-row>
    </b-container>
    <div>
      <p class="text_warning" v-for="item in errors" :key="item.id">{{ item }}</p>
    </div>
    <b-container fluid>
      <b-row>
        <b-col lg="6" class="my-1">
          <b-form-group
            label="Filter"
            label-for="filter-input"
            label-cols-sm="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-0"
          >
            <b-input-group size="sm">
              <b-form-input
                id="filter-input"
                v-model="filter"
                type="search"
                placeholder="Type to Search"
              ></b-form-input>

              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
        </b-col>
      </b-row>
      <b-table
        class="jig-table"
        hover
        responsive
        no-border-collapse
        :busy="tableBusy"
        :items="tableItems"
        :fields="tableFields"
        :sort-by.sync="tableSortBy"
        :sort-desc.sync="tableSortDesc"
        :filter="filter"
        :filter-included-fields="filterOn"
      >
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
        <template #cell(actions)="row">
          <b-dropdown
            :disabled="isJigTableButtonDisabled(row)"
            split
            @click="reserveJig(row.item)"
            class="m-2"
          >
            <template #button-content>{{jigTableButtonName(row)}}</template>
            <b-dropdown-item>Update</b-dropdown-item>
            <b-dropdown-item>Delete</b-dropdown-item>
            <b-dropdown-item @click="viewJig(row)">{{ row.detailsShowing ? 'Hide' : 'Show'}} View</b-dropdown-item>
          </b-dropdown>
        </template>
        <template #row-details="row">
          <div class="text-center text-danger my-2" v-if="jigDetailsBusy">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
          <div v-else>
            <b-card>
              <b-row class="mb-2">
                <b-col sm="3" class="text-sm-right">
                  <b>Location:</b>
                </b-col>
                <b-col>{{ jigViewDetails.location }}</b-col>
              </b-row>

              <b-row class="mb-2">
                <b-col sm="3" class="text-sm-right">
                  <b>No of CEPs:</b>
                </b-col>
                <b-col>{{ jigViewDetails.cepList.length }}</b-col>
              </b-row>

              <b-row class="mb-2">
                <b-col sm="3" class="text-sm-right">
                  <b>Jig Type:</b>
                </b-col>
                <b-col>{{ jigViewDetails.jigType }}</b-col>
              </b-row>

              <b-button size="sm" @click="row.toggleDetails">Hide Details</b-button>
            </b-card>
          </div>
        </template>
      </b-table>
    </b-container>
    <div></div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);
export default {
  name: "JigManager",
  created() {
    console.log("Created JigManager ");
    this.tableBusy = true;
    this.getJigDetails();
  },
  mounted() {},
  destroyed() {
    console.log("Destroyed Jig Manager");
  },
  data() {
    return {
      errors: [],
      tableFields: [
        { key: "jigid", sortable: true, label: "Jig ID" },
        { key: "jigname", sortable: true, label: "Jig Name" },
        { key: "owner", sortable: true, label: "Owner" },
        { key: "status", sortable: true, label: "Status" },
        { key: "actions", sortable: false, label: "Actions" }
      ],
      tableItems: [
        { jigid: 1, jigname: "testjig1", owner: "None", status: "Idle" }
      ],
      tableBusy: false,
      tableSortBy: "jigid",
      tableSortDesc: false,
      filter: null,
      filterOn: [],
      jigViewDetails: {},
      jigDetailsBusy: false
    };
  },
  methods: {
    getJigDetails(e) {
      this.errors = [];
      this.axios
        .get("/getjigtable")
        .then(resp => {
          console.log(resp);
          if (resp.data.status == true) {
            this.tableBusy = false;
            console.log("table data recieved");
            this.tableItems = resp.data.rslt;
            console.log(this.tableItems);
          } else {
            this.errors.push(resp.data.error);
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.errors.push(error);
        });
      //   e.preventDefault();
    },
    reserveJig(item) {
      console.log(
        "Reserve Jig",
        item.jigid,
        "for",
        this.$store.state.userData.username
      );
      var apiData = {
        jigid: item.jigid,
        jigowner: this.$store.state.userData.username
      };
      this.errors = [];
      this.axios
        .post("/postreservejig", apiData)
        .then(result => {
          console.log(result);
          if (result.data.status == true) {
            console.log("Jig Reservation Queued");
            alert(
              "Jig Reservation request has been queued. Please check back in a while"
            );
            this.jigViewDetails = result.data.rslt;
            this.jigDetailsBusy = false;
          } else {
            this.errors.push(result.data.error);
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.errors.push(error);
        });
    },
    viewJig(row) {
      row.toggleDetails();
      this.jigDetailsBusy = true;
      console.log("View Jig", row.item.jigid);
      this.errors = [];
      this.axios
        .post("/postjigdetails", row.item)
        .then(result => {
          console.log(result);
          if (result.data.status == true) {
            console.log("jig details received");
            this.jigViewDetails = result.data.rslt;
            this.jigDetailsBusy = false;
          } else {
            this.errors.push(result.data.error);
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.errors.push(error);
        });
    },
    jigTableButtonName(row) {
      if (row.item.status == "Idle") {
        return "Reserve";
      } else if (row.item.status == "Reserved") {
        return "Release";
      }
    },
    isJigTableButtonDisabled(row) {
      if (row.item.owner == "None") {
        return false;
      } else if (row.item.owner != this.$store.state.userData.username) {
        return true;
      } else {
        return false;
      }
    }
  }
};
</script>
<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background: whitesmoke !important;
}

.add-jig-btn {
  float: right;
  margin-right: 5%;
}
.row {
  margin-top: 1%;
}
.col-8 h3 {
  margin-left: 40%;
  align-content: center;
}

/* .jig-table {
  margin-top: 2%;
} */
</style>
