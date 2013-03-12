using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using WikiGolem.Models;
using System.Data.SqlClient;

namespace WikiGolem.Controllers
{
    public class Top10Controller : ApiController
    {
        GolemEntities contextTop10 = new GolemEntities();

        public IEnumerable<Top10> getWikiTop10Data()
        {
            Top10[] top10 = contextTop10.Database.SqlQuery<Top10>("select top 25 Name, sum(Pagecount) as Pagecount from wikidata where Name NOT in ('Wiki',';','Main_Page/',');') group by Name order by sum(Pagecount) desc").ToArray<Top10>();
            return top10;
        }
    }
}
