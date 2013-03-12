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
    public class WikiController : ApiController
    {
        GolemEntities context = new GolemEntities();

        public IEnumerable<WikiData> getWikiTop10Data(String date)
        {
            WikiData[] wiki = context.Database.SqlQuery<WikiData>("select sub1.Name, w.wikiDate, sum(w.Pagecount) as Pagecount from wikidata w inner join (select top 10 Name from wikidata where wikiDate = @param1 and Name NOT in ('404_error', ';', ');','Main_Page/','Wiki',',') order by  Pagecount desc) sub1 on w.Name = sub1.Name group by sub1.Name, w.wikiDate", new SqlParameter("param1", date)).ToArray<WikiData>();
            return wiki;
        }
    }
}
